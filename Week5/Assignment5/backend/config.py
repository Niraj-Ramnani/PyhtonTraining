import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

class Config:
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = int(os.environ.get("DB_PORT", 5432))
    DB_NAME = os.environ.get("DB_NAME", "food_ordering")
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "100")
    DATABASE_URL = os.environ.get("DATABASE_URL")

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "change-this-secret-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24
