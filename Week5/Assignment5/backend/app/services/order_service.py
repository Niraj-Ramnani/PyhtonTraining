from db import get_db


def create_order(user_id, restaurant_id, items, payment_method="cash"):
    conn = get_db()
    try:
        total = 0
        resolved_items = []
        with conn.cursor() as cur:
            cur.execute("SELECT user_id, name FROM Users WHERE user_id = %s", (user_id,))
            user = cur.fetchone()
            if user is None:
                raise ValueError(f"Customer with ID {user_id} does not exist")

            cur.execute("SELECT restaurant_id, name FROM Restaurants WHERE restaurant_id = %s", (restaurant_id,))
            restaurant = cur.fetchone()
            if restaurant is None:
                raise ValueError(f"Restaurant with ID {restaurant_id} does not exist")

            if not items or not isinstance(items, list):
                raise ValueError("Order must contain a non-empty list of items")

            for item in items:
                food_item_id = item.get("food_item_id") or item.get("id")
                if not food_item_id:
                    raise ValueError("Each item must have a valid food_item_id")

                quantity = item.get("quantity")
                if not isinstance(quantity, int) or quantity <= 0:
                    raise ValueError(f"Quantity for food_item_id {food_item_id} must be a positive integer")

                cur.execute(
                    "SELECT price, restaurant_id, is_available, name FROM Food_Items WHERE food_item_id = %s",
                    (food_item_id,),
                )
                food = cur.fetchone()
                if food is None:
                    raise ValueError(f"Food item {food_item_id} does not exist")
                if food["restaurant_id"] != restaurant_id:
                    raise ValueError(f"Food item '{food['name']}' (ID {food_item_id}) does not belong to restaurant {restaurant_id}")
                if not food["is_available"]:
                    raise ValueError(f"Food item '{food['name']}' (ID {food_item_id}) is currently unavailable")

                price = float(food["price"])
                total += price * quantity
                resolved_items.append((food_item_id, quantity, price))

            total_amount = round(total, 2)

            cur.execute(
                "INSERT INTO Orders (user_id, restaurant_id, order_status, total_amount) "
                "VALUES (%s, %s, 'pending', %s) RETURNING order_id, order_status, created_at",
                (user_id, restaurant_id, total_amount),
            )
            order_row = cur.fetchone()
            order_id = order_row["order_id"]

            for food_item_id, quantity, price in resolved_items:
                cur.execute(
                    "INSERT INTO Order_Items (order_id, food_item_id, quantity, price_at_order) "
                    "VALUES (%s, %s, %s, %s)",
                    (order_id, food_item_id, quantity, price),
                )

            payment_status = "completed" if payment_method in ["card", "upi"] else "pending"
            cur.execute(
                "INSERT INTO Payments (order_id, amount, payment_method, payment_status) "
                "VALUES (%s, %s, %s, %s) RETURNING payment_id",
                (order_id, total_amount, payment_method, payment_status),
            )

        conn.commit()
        return get_order_by_id(order_id)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_order_by_id(order_id, user_id=None):
    conn = get_db()
    with conn.cursor() as cur:
        query = "SELECT * FROM Orders WHERE order_id = %s"
        params = [order_id]
        if user_id is not None:
            query += " AND user_id = %s"
            params.append(user_id)
        cur.execute(query, tuple(params))
        order = cur.fetchone()
        if order is None:
            conn.close()
            return None

        cur.execute(
            """
            SELECT oi.food_item_id, f.name, oi.quantity, oi.price_at_order
            FROM Order_Items oi
            JOIN Food_Items f ON f.food_item_id = oi.food_item_id
            WHERE oi.order_id = %s
            """,
            (order_id,),
        )
        items = cur.fetchall()

        cur.execute("SELECT * FROM Payments WHERE order_id = %s", (order_id,))
        payment = cur.fetchone()
    conn.close()

    order_dict = dict(order)
    order_dict["items"] = [dict(i) for i in items]
    order_dict["payment"] = dict(payment) if payment else None
    return order_dict


def get_orders_for_user(user_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT order_id FROM Orders WHERE user_id = %s ORDER BY created_at DESC", (user_id,)
        )
        rows = cur.fetchall()
    conn.close()
    return [get_order_by_id(r["order_id"]) for r in rows]


def update_order_status(order_id, status):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE Orders SET order_status = %s WHERE order_id = %s", (status, order_id)
        )
        updated = cur.rowcount > 0
    conn.commit()
    conn.close()
    if not updated:
        return None
    return get_order_by_id(order_id)
