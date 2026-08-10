# Week 4 Assignment — Online Food Ordering REST API

Database-driven enhancement of the Week 3 Flask REST API using PostgreSQL.

## Included

- Relational schema and 3NF
- SQL DDL and verification
- Seed data
- JOINs and subqueries
- SQL reports
- Indexes and `EXPLAIN ANALYZE`
- PostgreSQL transaction/function for Place Order
- Views
- PostgreSQL functions
- Triggers
- JWT authentication
- Role-based authorization
- Input validation
- CRUD APIs
- Postman collection
- ERD and normalization documentation
- Performance report template

## Project structure

```text
online_food_ordering_week4/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── sql/
└── docs/
    └── api.md, erd.md, normalization.md, performance_report.md
└── postman/
    └── food-ordering.postman_collection.json
```

## Setup

1. Create the PostgreSQL database:
```sql
CREATE DATABASE food_ordering;
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install:
```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and set your PostgreSQL password.

5. Execute the SQL scripts in dependency order:
```text
01_schema.sql
02_verify.sql
03_seed.sql
04_queries_joins.sql
05_subqueries.sql
06_reports.sql
07_indexes_performance.sql
08_transaction_function.sql
09_views.sql
10_triggers.sql
11_sample_function_calls.sql
12_trigger_tests.sql
```

6. Run:
```bash
python app.py
```

## Demo login

```text
Email: user1@example.com
Password: Password@123
```

## Assignment mapping

| Task | Implementation |
|---|---|
| 1 Schema | `sql/01_schema.sql` |
| 2 DDL + verification | `01_schema.sql`, `02_verify.sql` |
| 3 ERD + 3NF | `docs/erd.md`, `docs/normalization.md` |
| 4 Database APIs | `app.py` |
| 5 Seed data | `03_seed.sql` |
| 6 JOINs | `04_queries_joins.sql` |
| 7 Subqueries | `05_subqueries.sql` |
| 8 Reports | `06_reports.sql` |
| 9 Performance | `07_indexes_performance.sql` |
| 10 Transactions/ACID | `08_transaction_function.sql` |
| 11 Views | `09_views.sql` |
| 12 Functions | `08_transaction_function.sql` |
| 13 Triggers | `10_triggers.sql` |
| 14 Final project | Entire repository |

## GitHub

Do not commit `.env`.

```bash
git init
git add .
git commit -m "Complete Week 4 database integrated food ordering API"
git branch -M main
git remote add origin <your-repository-url>
git push -u origin main
```
