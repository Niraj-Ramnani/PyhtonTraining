# Online Food Ordering System

A learning project built for a relational database backend assignment: a Flask REST API
backed by a proper relational (3NF) **PostgreSQL** database, plus a React + TypeScript
frontend that consumes it.

```
foodorder-project/
  backend/     Flask API + PostgreSQL database (see backend/README.md)
  frontend/    React + TypeScript client (see frontend/README.md)
```

## Quick start

### 1. Database & Backend (runs on http://127.0.0.1:5000)
1. Ensure PostgreSQL is running (default port `5432`).
2. Configure credentials in `backend/.env`:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=food_ordering
   DB_USER=postgres
   DB_PASSWORD=100
   JWT_SECRET_KEY=food-ordering-jwt-secret-key-2026
   ```
3. Install dependencies, seed database, and run server:
   ```bash
   cd backend
   pip install -r requirements.txt
   python seed.py
   python run.py
   ```

### 2. Frontend (runs on http://127.0.0.1:5173), in a second terminal
```bash
cd frontend
npm install
npm run dev
```

Then open [http://127.0.0.1:5173](http://127.0.0.1:5173) in your browser.

### Seeded Accounts
- **Customer**: `aarav@example.com` / `Password@123`
- **Admin**: `admin@example.com` / `Admin@123` (admin can create/update/delete restaurants & food items, update order statuses, and view the reports in `backend/subqueries.sql` via `/api/reports/*`)

---

## Features & Implementation Details

| Requirement | Where |
|---|---|
| Relational schema, 3NF, PK/FK/UNIQUE/CHECK/DEFAULT | `backend/schema.sql` |
| PostgreSQL connection & auto-initialization | `backend/db.py` |
| Register/Login/Restaurant/Food/Order/Profile via SQL CRUD | `backend/app/routes/*` calling `backend/app/services/*` |
| Seed data (10 users, 5 restaurants, 5 categories, 30 items, 20 orders, 20 payments) | `backend/seed.py` |
| 5 required subqueries | `backend/subqueries.sql` and `backend/app/services/report_service.py` (exposed as `/api/reports/*`) |
