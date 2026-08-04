import sqlite3

connection = sqlite3.connect("employee.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employee(
    id INTEGER PRIMARY KEY,
    name TEXT,
    salary INTEGER
)
""")

cursor.execute(
    "INSERT INTO employee VALUES (?, ?, ?)",
    (101, "employe1", 50000)
)

cursor.execute("SELECT * FROM employee")

for employee in cursor.fetchall():
    print(employee)

connection.commit()
connection.close()