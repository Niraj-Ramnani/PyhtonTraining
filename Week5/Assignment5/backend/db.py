import os
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import Config


def _get_connection_params(db_name=None):
    if Config.DATABASE_URL:
        return {"dsn": Config.DATABASE_URL}
    return {
        "host": Config.DB_HOST,
        "port": Config.DB_PORT,
        "dbname": db_name or Config.DB_NAME,
        "user": Config.DB_USER,
        "password": Config.DB_PASSWORD,
    }


def ensure_database_exists():
    if Config.DATABASE_URL:
        return

    target_db = Config.DB_NAME
    params = _get_connection_params(db_name="postgres")
    try:
        conn = psycopg2.connect(**params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (target_db,))
        exists = cur.fetchone()
        if not exists:
            cur.execute(f'CREATE DATABASE "{target_db}"')
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database check/creation notice: {e}")


def get_db():
    params = _get_connection_params()
    conn = psycopg2.connect(**params, cursor_factory=RealDictCursor)
    return conn


def init_db():
    ensure_database_exists()
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(schema_sql)
    conn.commit()
    conn.close()
