from db import get_db


def get_food_items(restaurant_id=None, category_id=None):
    query = """
        SELECT f.*, c.category_name, r.name AS restaurant_name
        FROM Food_Items f
        JOIN Categories c ON c.category_id = f.category_id
        JOIN Restaurants r ON r.restaurant_id = f.restaurant_id
        WHERE 1 = 1
    """
    params = []
    if restaurant_id:
        query += " AND f.restaurant_id = %s"
        params.append(restaurant_id)
    if category_id:
        query += " AND f.category_id = %s"
        params.append(category_id)
    query += " ORDER BY f.name"

    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_food_item_by_id(food_item_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Food_Items WHERE food_item_id = %s", (food_item_id,))
        row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def create_food_item(restaurant_id, category_id, name, price, is_available=1):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO Food_Items (restaurant_id, category_id, name, price, is_available) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING food_item_id",
            (restaurant_id, category_id, name, float(price), is_available),
        )
        new_id = cur.fetchone()["food_item_id"]
    conn.commit()
    conn.close()
    return get_food_item_by_id(new_id)


def update_food_item(food_item_id, name, price, is_available):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE Food_Items SET name = %s, price = %s, is_available = %s WHERE food_item_id = %s",
            (name, float(price), is_available, food_item_id),
        )
    conn.commit()
    conn.close()
    return get_food_item_by_id(food_item_id)


def delete_food_item(food_item_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM Food_Items WHERE food_item_id = %s", (food_item_id,))
        deleted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def get_all_categories():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Categories ORDER BY category_name")
        rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
