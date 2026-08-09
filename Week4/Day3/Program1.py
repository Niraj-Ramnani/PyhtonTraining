import psycopg


def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="company_db",
        user="postgres",
        password="100"
    )


def print_employees(title, query, parameters=()):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query, parameters)

    employees = cursor.fetchall()

    print(f"\n--- {title} ---")

    for employee in employees:
        print(employee)

    cursor.close()
    connection.close()


# 1. Salary greater than 50,000
print_employees(
    "Employees with salary > 50000",
    """
    SELECT id, name, salary, department_id
    FROM employees
    WHERE salary > %s
    ORDER BY salary DESC;
    """,
    (50000,)
)


# 2. Employees between age 25 and 30
print_employees(
    "Employees between age 25 and 30",
    """
    SELECT id, name, age, salary
    FROM employees
    WHERE age BETWEEN %s AND %s
    ORDER BY age;
    """,
    (25, 30)
)


# 3. Employees from IT or Finance
print_employees(
    "Employees from IT or Finance",
    """
    SELECT e.id, e.name, e.salary, d.name
    FROM employees e
    JOIN departments d
        ON e.department_id = d.id
    WHERE d.name IN (%s, %s)
    ORDER BY e.name;
    """,
    ("IT", "Finance")
)


# 4. Employees whose name starts with R
print_employees(
    "Employees whose name starts with R",
    """
    SELECT id, name, email
    FROM employees
    WHERE name LIKE %s;
    """,
    ("R%",)
)


# 5. Top 3 highest-paid employees
print_employees(
    "Top 3 highest-paid employees",
    """
    SELECT id, name, salary
    FROM employees
    ORDER BY salary DESC
    LIMIT 3;
    """
)