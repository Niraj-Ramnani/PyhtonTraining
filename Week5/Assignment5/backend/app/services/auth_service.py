from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db


def get_user_by_email(email):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Users WHERE email = %s", (email,))
        user = cur.fetchone()
    conn.close()
    return dict(user) if user else None


def create_user(name, email, password, phone=None):
    if get_user_by_email(email) is not None:
        return None

    password_hash = generate_password_hash(password)
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO Users (name, email, password_hash, phone, role_id) VALUES (%s, %s, %s, %s, 1) RETURNING user_id",
            (name, email, password_hash, phone),
        )
        row = cur.fetchone()
        user_id = row["user_id"]
    conn.commit()
    conn.close()
    return user_id


def verify_login(email, password):
    user = get_user_by_email(email)
    if user is None:
        return None
    if not check_password_hash(user["password_hash"], password):
        return None
    return user


def get_role_name(role_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT role_name FROM Roles WHERE role_id = %s", (role_id,))
        role = cur.fetchone()
    conn.close()
    return role["role_name"] if role else "customer"
