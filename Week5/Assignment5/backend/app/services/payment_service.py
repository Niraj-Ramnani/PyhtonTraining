from db import get_db


def create_payment(order_id, amount, payment_method):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO Payments (order_id, amount, payment_method, payment_status) "
            "VALUES (%s, %s, %s, 'completed') RETURNING payment_id",
            (order_id, float(amount), payment_method),
        )
        payment_id = cur.fetchone()["payment_id"]
        cur.execute("SELECT * FROM Payments WHERE payment_id = %s", (payment_id,))
        row = cur.fetchone()
    conn.commit()
    conn.close()
    return dict(row) if row else None


def get_payment_for_order(order_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Payments WHERE order_id = %s", (order_id,))
        row = cur.fetchone()
    conn.close()
    return dict(row) if row else None
