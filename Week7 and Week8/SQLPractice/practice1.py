import psycopg2

admin_conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="100",
)
admin_conn.autocommit = True
admin_cursor = admin_conn.cursor()
admin_cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'sql_practice'")
if admin_cursor.fetchone() is None:
    admin_cursor.execute("CREATE DATABASE sql_practice")
admin_cursor.close()
admin_conn.close()

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="sql_practice",
    user="postgres",
    password="100",
)

cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS enrollments")
cursor.execute("DROP TABLE IF EXISTS courses")
cursor.execute("DROP TABLE IF EXISTS students")

cursor.execute(
    """
    CREATE TABLE students (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        age INT NOT NULL,
        city VARCHAR(50),
        grade CHAR(1) DEFAULT 'B'
    )
    """
)

cursor.execute(
    """
    CREATE TABLE courses (
        course_id SERIAL PRIMARY KEY,
        course_name VARCHAR(50) NOT NULL,
        credits INT NOT NULL CHECK (credits > 0)
    )
    """
)

cursor.execute(
    """
    CREATE TABLE enrollments (
        student_id INT NOT NULL,
        course_id INT NOT NULL,
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (course_id) REFERENCES courses(course_id)
    )
    """
)

students = [
    ("Rahul", 20, "Pune", "A"),
    ("Neha", 22, "Delhi", "B"),
    ("Amit", 21, "Mumbai", "A"),
    ("Pooja", 19, "Pune", "C"),
    ("Ravi", 23, "Nagpur", "B"),
]

cursor.executemany(
    "INSERT INTO students (name, age, city, grade) VALUES (%s, %s, %s, %s)",
    students,
)

courses = [
    ("SQL Basics", 3),
    ("Python for Data", 4),
    ("Database Design", 3),
]

cursor.executemany(
    "INSERT INTO courses (course_name, credits) VALUES (%s, %s)",
    courses,
)

enrollments = [
    (1, 1),
    (1, 2),
    (2, 1),
    (3, 3),
    (4, 2),
    (5, 1),
]

cursor.executemany(
    "INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)",
    enrollments,
)

conn.commit()

queries = [
    "SELECT * FROM students ORDER BY id",
    "SELECT name, city FROM students WHERE city = 'Pune' ORDER BY name",
    "SELECT COUNT(*) FROM students WHERE age >= 20",
    "SELECT AVG(age) AS average_age FROM students",
    "SELECT city, COUNT(*) AS total_students FROM students GROUP BY city ORDER BY total_students DESC",
    "UPDATE students SET city = 'Nagpur' WHERE name = 'Rahul'",
    "SELECT * FROM students WHERE name = 'Rahul'",
    "DELETE FROM students WHERE id = 5",
    "SELECT * FROM students ORDER BY id",
    "SELECT s.name, c.course_name FROM students s JOIN enrollments e ON s.id = e.student_id JOIN courses c ON c.course_id = e.course_id ORDER BY s.name",
    "SELECT c.course_name, COUNT(e.student_id) AS total_students FROM courses c LEFT JOIN enrollments e ON c.course_id = e.course_id GROUP BY c.course_name ORDER BY total_students DESC",
]

for query in queries:
    cursor.execute(query)
    if query.lower().startswith("select"):
        rows = cursor.fetchall()
        print(query)
        for row in rows:
            print(row)
        print()
    else:
        conn.commit()
        print(query)
        print("done")
        print()

cursor.close()
conn.close()