import random
from werkzeug.security import generate_password_hash
from db import get_db, init_db

def seed():
    init_db()
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "TRUNCATE TABLE Payments, Order_Items, Orders, Food_Items, Categories, Restaurants, Users RESTART IDENTITY CASCADE;"
    )

    users = [
        ("Aarav Sharma", "aarav@example.com"), ("Diya Patel", "diya@example.com"),
        ("Vihaan Gupta", "vihaan@example.com"), ("Ananya Singh", "ananya@example.com"),
        ("Arjun Kumar", "arjun@example.com"), ("Ishita Rao", "ishita@example.com"),
        ("Kabir Mehta", "kabir@example.com"), ("Saanvi Joshi", "saanvi@example.com"),
        ("Reyansh Nair", "reyansh@example.com"), ("Myra Verma", "myra@example.com"),
    ]
    password_hash = generate_password_hash("Password@123")
    user_ids = []
    for name, email in users:
        cur.execute(
            "INSERT INTO Users (name, email, password_hash, phone, role_id) VALUES (%s, %s, %s, %s, 1) RETURNING user_id",
            (name, email, password_hash, f"9{random.randint(100000000, 999999999)}"),
        )
        user_ids.append(cur.fetchone()["user_id"])

    cur.execute(
        "INSERT INTO Users (name, email, password_hash, phone, role_id) VALUES (%s, %s, %s, %s, 2) RETURNING user_id",
        ("Admin User", "admin@example.com", generate_password_hash("Admin@123"), "9999999999"),
    )

    restaurants = [
        ("Spice Villa", "MI Road, Jaipur", "9811111111"),
        ("Curry House", "C-Scheme, Jaipur", "9822222222"),
        ("Pizza Point", "Vaishali Nagar, Jaipur", "9833333333"),
        ("Burger Barn", "Malviya Nagar, Jaipur", "9844444444"),
        ("South Spice", "Tonk Road, Jaipur", "9855555555"),
    ]
    restaurant_ids = []
    for name, address, phone in restaurants:
        cur.execute(
            "INSERT INTO Restaurants (name, address, phone, rating) VALUES (%s, %s, %s, %s) RETURNING restaurant_id",
            (name, address, phone, round(random.uniform(3.5, 5.0), 1)),
        )
        restaurant_ids.append(cur.fetchone()["restaurant_id"])

    categories = ["Starters", "Main Course", "Beverages", "Desserts", "Fast Food"]
    category_ids = []
    for c in categories:
        cur.execute("INSERT INTO Categories (category_name) VALUES (%s) RETURNING category_id", (c,))
        category_ids.append(cur.fetchone()["category_id"])

    item_names = [
        "Paneer Tikka", "Veg Spring Roll", "Butter Chicken", "Dal Makhani",
        "Masala Chai", "Cold Coffee", "Gulab Jamun", "Ice Cream Sundae",
        "Cheese Burger", "French Fries",
    ]
    food_item_ids = []
    for r_id in restaurant_ids:
        for i in range(6):
            name = random.choice(item_names)
            category_id = random.choice(category_ids)
            price = round(random.uniform(80, 450), 2)
            cur.execute(
                "INSERT INTO Food_Items (restaurant_id, category_id, name, price, is_available) "
                "VALUES (%s, %s, %s, %s, 1) RETURNING food_item_id",
                (r_id, category_id, name, price),
            )
            food_item_ids.append((cur.fetchone()["food_item_id"], r_id, price))

    payment_methods = ["cash", "card", "upi"]
    statuses = ["pending", "confirmed", "delivered", "cancelled"]

    for _ in range(20):
        user_id = random.choice(user_ids)
        r_id = random.choice(restaurant_ids)
        items_for_restaurant = [f for f in food_item_ids if f[1] == r_id]
        chosen_items = random.sample(items_for_restaurant, k=min(3, len(items_for_restaurant)))

        total = 0
        order_items_data = []
        for food_item_id, _, price in chosen_items:
            qty = random.randint(1, 3)
            total += price * qty
            order_items_data.append((food_item_id, qty, price))

        cur.execute(
            "INSERT INTO Orders (user_id, restaurant_id, order_status, total_amount) VALUES (%s, %s, %s, %s) RETURNING order_id",
            (user_id, r_id, random.choice(statuses), round(total, 2)),
        )
        order_id = cur.fetchone()["order_id"]

        for food_item_id, qty, price in order_items_data:
            cur.execute(
                "INSERT INTO Order_Items (order_id, food_item_id, quantity, price_at_order) "
                "VALUES (%s, %s, %s, %s)",
                (order_id, food_item_id, qty, price),
            )

        cur.execute(
            "INSERT INTO Payments (order_id, amount, payment_method, payment_status) VALUES (%s, %s, %s, %s)",
            (order_id, round(total, 2), random.choice(payment_methods), random.choice(["pending", "completed", "failed"])),
        )

    conn.commit()
    cur.close()
    conn.close()
    print("PostgreSQL Database seeded: 10 users (+1 admin), 5 restaurants, 5 categories, 30 food items, 20 orders, 20 payments.")


if __name__ == "__main__":
    seed()
