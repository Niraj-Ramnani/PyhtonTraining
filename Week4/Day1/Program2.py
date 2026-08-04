import sqlite3

connection = sqlite3.connect("student.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    course TEXT
)
""")

students = [
    ("Neeraj", 22, "Python"),
]

cursor.executemany(
    "INSERT INTO students(name, age, course) VALUES (?, ?, ?)",
    students
)

connection.commit()

cursor.execute("SELECT * FROM students")

print("Student Records:\n")

for student in cursor.fetchall():
    print(student)

connection.close()