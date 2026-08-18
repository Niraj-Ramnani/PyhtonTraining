# Online Food Ordering - Backend (Flask + PostgreSQL)

## Setup
1. Configure `backend/.env` with your PostgreSQL database details:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=food_ordering
DB_USER=postgres
DB_PASSWORD=100
JWT_SECRET_KEY=food-ordering-jwt-secret-key-2026
```

2. Run the application:
```bash
cd backend
pip install -r requirements.txt
python seed.py                # creates + populates food_ordering PostgreSQL DB
python run.py                 # starts server on http://127.0.0.1:5000
```

## Project structure
```
backend/
  .env                 # environment variables (PostgreSQL credentials, JWT secret)
  .env.example         # sample environment configuration
  config.py            # loads .env and provides Flask Config
  db.py                # PostgreSQL connection + auto-database and table creation
  schema.sql           # PostgreSQL table definitions (PK, FK, UNIQUE, CHECK, DEFAULT)
  seed.py              # sample data (10 users, 5 restaurants, 5 categories,
                       # 30 food items, 20 orders, 20 payments)
  subqueries.sql       # the 5 required reporting subqueries, as standard SQL
  run.py               # server entry point
  app/
    __init__.py        # Flask app factory, blueprint registration
    routes/            # HTTP layer - request parsing, status codes
    services/          # SQL layer - all database queries live here
    utils/             # validators + role-check decorator
```

## Default accounts (after seeding)
- Admin: `admin@example.com` / `Admin@123`
- Customer: `aarav@example.com` / `Password@123` (all seeded customers use this password)

## API overview
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | /api/auth/register | none | create a customer account |
| POST | /api/auth/login | none | returns a JWT |
| GET | /api/restaurants | none | list restaurants |
| POST/PUT/DELETE | /api/restaurants | admin | manage restaurants |
| GET | /api/food-items?restaurant_id=&category_id= | none | menu listing |
| POST/PUT/DELETE | /api/food-items | admin | manage menu items |
| POST | /api/orders | customer | place an order |
| GET | /api/orders | customer | list your own orders |
| GET | /api/orders/<id> | customer/admin | order detail |
| PUT | /api/orders/<id>/status | admin | update order status |
| GET | /api/profile | customer | view your profile |
| PUT | /api/profile | customer | update name/phone |
| GET | /api/reports/* | admin | the 5 required subqueries |

All protected endpoints expect `Authorization: Bearer <token>`.
