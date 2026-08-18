from db import get_db


def get_profile(user_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT u.user_id, u.name, u.email, u.phone, r.role_name, u.created_at
            FROM Users u
            JOIN Roles r ON r.role_id = u.role_id
            WHERE u.user_id = %s
            """,
            (user_id,),
        )
        row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def update_profile(user_id, name, phone):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE Users SET name = %s, phone = %s WHERE user_id = %s",
            (name, phone, user_id),
        )
    conn.commit()
    conn.close()
    return get_profile(user_id)
