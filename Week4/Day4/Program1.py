import psycopg


def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="company_db",
        user="postgres",
        password="100"
    )


def execute_query(title, query):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query)
    results = cursor.fetchall()

    print(f"\n--- {title} ---")

    for row in results:
        print(row)

    cursor.close()
    connection.close()


execute_query(
    "Employees with Department",
    """
    SELECT
        e.id,
        e.name,
        e.email,
        e.salary,
        d.name AS department
    FROM employees e
    INNER JOIN departments d
        ON e.department_id = d.id
    ORDER BY e.id;
    """
)


execute_query(
    "All Departments",
    """
    SELECT
        d.id,
        d.name,
        e.name AS employee
    FROM departments d
    LEFT JOIN employees e
        ON d.id = e.department_id
    ORDER BY d.id;
    """
)


execute_query(
    "Employees Above Average Salary",
    """
    SELECT
        id,
        name,
        salary
    FROM employees
    WHERE salary > (
        SELECT AVG(salary)
        FROM employees
    )
    ORDER BY salary DESC;
    """
)


execute_query(
    "Highest Paid Employee Per Department",
    """
    SELECT
        e.name,
        e.salary,
        d.name AS department
    FROM employees e
    JOIN departments d
        ON e.department_id = d.id
    WHERE e.salary = (
        SELECT MAX(e2.salary)
        FROM employees e2
        WHERE e2.department_id = e.department_id
    )
    ORDER BY d.name;
    """
)