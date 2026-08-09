from flask import Flask, jsonify
import psycopg


app = Flask(__name__)


def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="company_db",
        user="postgres",
        password="your_password"
    )


@app.get("/employees")
def get_employees():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            e.id,
            e.name,
            e.email,
            e.age,
            e.salary,
            d.name AS department
        FROM employees e
        JOIN departments d
            ON e.department_id = d.id
        ORDER BY e.id;
        """
    )

    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    result = []

    for employee in employees:
        result.append({
            "id": employee[0],
            "name": employee[1],
            "email": employee[2],
            "age": employee[3],
            "salary": float(employee[4]),
            "department": employee[5]
        })

    return jsonify(result)


@app.get("/employees/<int:employee_id>")
def get_employee(employee_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            e.id,
            e.name,
            e.email,
            e.age,
            e.salary,
            d.name AS department
        FROM employees e
        JOIN departments d
            ON e.department_id = d.id
        WHERE e.id = %s;
        """,
        (employee_id,)
    )

    employee = cursor.fetchone()

    cursor.close()
    connection.close()

    if employee is None:
        return jsonify({
            "error": "Employee not found"
        }), 404

    return jsonify({
        "id": employee[0],
        "name": employee[1],
        "email": employee[2],
        "age": employee[3],
        "salary": float(employee[4]),
        "department": employee[5]
    })


@app.get("/departments/<int:department_id>/employees")
def get_department_employees(department_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            e.id,
            e.name,
            e.email,
            e.salary
        FROM employees e
        WHERE e.department_id = %s
        ORDER BY e.salary DESC;
        """,
        (department_id,)
    )

    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    result = []

    for employee in employees:
        result.append({
            "id": employee[0],
            "name": employee[1],
            "email": employee[2],
            "salary": float(employee[3])
        })

    return jsonify(result)


@app.get("/employees/above-average")
def get_above_average_employees():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
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

    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    result = []

    for employee in employees:
        result.append({
            "id": employee[0],
            "name": employee[1],
            "salary": float(employee[2])
        })

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)