from db import get_db


def get_all_restaurants():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Restaurants ORDER BY name")
        rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_restaurant_by_id(restaurant_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Restaurants WHERE restaurant_id = %s", (restaurant_id,))
        row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def create_restaurant(name, address, phone, rating=0):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO Restaurants (name, address, phone, rating) VALUES (%s, %s, %s, %s) RETURNING restaurant_id",
            (name, address, phone, rating),
        )
        new_id = cur.fetchone()["restaurant_id"]
    conn.commit()
    conn.close()
    return get_restaurant_by_id(new_id)


def update_restaurant(restaurant_id, name, address, phone, rating):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE Restaurants SET name = %s, address = %s, phone = %s, rating = %s WHERE restaurant_id = %s",
            (name, address, phone, rating, restaurant_id),
        )
    conn.commit()
    conn.close()
    return get_restaurant_by_id(restaurant_id)


def delete_restaurant(restaurant_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM Restaurants WHERE restaurant_id = %s", (restaurant_id,))
        deleted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
