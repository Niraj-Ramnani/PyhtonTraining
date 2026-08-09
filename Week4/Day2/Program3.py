import psycopg


def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="company_db",
        user="postgres",
        password="100"
    )


def add_employee(name, email, age, salary, department_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO employees
        (name, email, age, salary, department_id)
        VALUES (%s, %s, %s, %s, %s);
        """,
        (name, email, age, salary, department_id)
    )

    connection.commit()

    cursor.close()
    connection.close()


def get_all_employees():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, email, age, salary, department_id
        FROM employees
        ORDER BY id;
        """
    )

    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    return employees


def get_employee_by_id(employee_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, email, age, salary, department_id
        FROM employees
        WHERE id = %s;
        """,
        (employee_id,)
    )

    employee = cursor.fetchone()

    cursor.close()
    connection.close()

    return employee


def update_salary(employee_id, new_salary):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE employees
        SET salary = %s
        WHERE id = %s;
        """,
        (new_salary, employee_id)
    )

    connection.commit()

    cursor.close()
    connection.close()


def delete_employee(employee_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM employees
        WHERE id = %s;
        """,
        (employee_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()


# Add employee
add_employee(
    "Karan",
    "karan@example.com",
    27,
    60000,
    1
)

# Display all employees
print("All employees:")

for employee in get_all_employees():
    print(employee)


# Find employee
employee = get_employee_by_id(1)

print("\nEmployee with ID 1:")
print(employee)


# Update salary
update_salary(1, 55000)

print("\nAfter salary update:")
print(get_employee_by_id(1))


# Delete employee
delete_employee(6)

print("\nAfter deletion:")

for employee in get_all_employees():
    print(employee)