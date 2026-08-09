# Question 1 — Connect Python to PostgreSQL and Create Database Tables
# creaing department and employment table

import psycopg


connection = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="company_db",
    user="postgres",
    password="100"
)

cursor = connection.cursor()

create_departments_table = """
CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);
"""

create_employees_table = """
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    age INTEGER CHECK (age >= 18),
    salary NUMERIC(10, 2) CHECK (salary > 0),
    department_id INTEGER,
    
    CONSTRAINT fk_department
        FOREIGN KEY (department_id)
        REFERENCES departments(id)
);
"""

cursor.execute(create_departments_table)
cursor.execute(create_employees_table)

connection.commit()

print("Tables created successfully.")

cursor.close()
connection.close()