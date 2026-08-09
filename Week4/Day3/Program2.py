import psycopg


def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="company_db",
        user="postgres",
        password="100"
    )


def generate_department_report():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        d.name AS department,
        COUNT(e.id) AS employee_count,
        SUM(e.salary) AS total_salary,
        ROUND(AVG(e.salary), 2) AS average_salary,
        MIN(e.salary) AS minimum_salary,
        MAX(e.salary) AS maximum_salary
    FROM departments d
    JOIN employees e
        ON d.id = e.department_id
    GROUP BY d.id, d.name
    HAVING COUNT(e.id) >= %s
       AND AVG(e.salary) > %s
    ORDER BY average_salary DESC;
    """

    cursor.execute(query, (2, 50000))

    reports = cursor.fetchall()

    print("\n--- Department Salary Report ---")

    for report in reports:
        print(
            f"Department: {report[0]}"
        )
        print(
            f"Employees: {report[1]}"
        )
        print(
            f"Total Salary: {report[2]}"
        )
        print(
            f"Average Salary: {report[3]}"
        )
        print(
            f"Minimum Salary: {report[4]}"
        )
        print(
            f"Maximum Salary: {report[5]}"
        )
        print("-" * 40)

    cursor.close()
    connection.close()


generate_department_report()