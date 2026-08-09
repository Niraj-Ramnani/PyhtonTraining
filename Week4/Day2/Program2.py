# Insert Data Using Parameterized Queries

import psycopg


connection = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="company_db",
    user="postgres",
    password="100"
)

cursor = connection.cursor()


departments = ["IT", "HR", "Finance"]

for department in departments:
    cursor.execute(
        """
        INSERT INTO departments (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING;
        """,
        (department,)
    )

cursor.execute(
    """
    SELECT id, name
    FROM departments;
    """
)

department_rows = cursor.fetchall()

department_map = {
    name: department_id
    for department_id, name in department_rows
}


# Employee data
employees = [
    ("Raju", "Raju@example.com", 25, 45000, "IT"),
    ("Amit", "amit@example.com", 30, 65000, "IT"),
]

for name, email, age, salary, department in employees:

    cursor.execute(
        """
        INSERT INTO employees
        (name, email, age, salary, department_id)
        VALUES (%s, %s, %s, %s, %s);
        """,
        (
            name,
            email,
            age,
            salary,
            department_map[department]
        )
    )


connection.commit()

print("Departments and employees inserted into table")

cursor.close()
connection.close()