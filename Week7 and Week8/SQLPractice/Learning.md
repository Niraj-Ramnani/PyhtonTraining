# SQL in Simple Language

SQL is a language used to talk to a database. It helps us create data, read data, update data, and delete data.

Think of a database like a big organized filing cabinet. Tables are like files, rows are records, and columns are the fields inside each record.

## 1. Basic SQL idea

- Database: a container for tables
- Table: a collection of related data
- Row: one record in a table
- Column: one field in a record

Example table:

students

| id | name | age | city |
| --- | --- | --- | --- |
| 1 | Rahul | 20 | Pune |
| 2 | Neha | 22 | Delhi |

## 2. Create a database

```sql
CREATE DATABASE school_db;
```

This creates a new database.

## 3. Create a table

```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    city VARCHAR(50),
    grade CHAR(1) DEFAULT 'B'
);
```

Important points:

- `SERIAL` gives automatic numbers
- `PRIMARY KEY` makes each row unique
- `NOT NULL` means the value cannot be empty
- `DEFAULT` gives a value if nothing is provided

## 4. Insert data

```sql
INSERT INTO students (name, age, city, grade)
VALUES ('Rahul', 20, 'Pune', 'A');
```

This adds one new record.

You can also insert multiple rows:

```sql
INSERT INTO students (name, age, city, grade)
VALUES
    ('Neha', 22, 'Delhi', 'B'),
    ('Amit', 21, 'Mumbai', 'A'),
    ('Pooja', 19, 'Pune', 'C');
```

## 5. Read data with SELECT

```sql
SELECT * FROM students;
```

This shows all columns and all rows.

To see only specific columns:

```sql
SELECT name, city FROM students;
```

To filter rows:

```sql
SELECT * FROM students WHERE city = 'Pune';
```

## 6. WHERE, AND, OR, NOT

```sql
SELECT * FROM students WHERE age >= 20;
```

```sql
SELECT * FROM students WHERE city = 'Pune' AND age > 20;
```

```sql
SELECT * FROM students WHERE city = 'Pune' OR city = 'Delhi';
```

```sql
SELECT * FROM students WHERE NOT city = 'Mumbai';
```

## 7. ORDER BY and LIMIT

```sql
SELECT * FROM students ORDER BY age DESC;
```

This sorts by age from highest to lowest.

```sql
SELECT * FROM students ORDER BY age ASC LIMIT 2;
```

This shows only the first 2 rows in sorted order.

## 8. DISTINCT

```sql
SELECT DISTINCT city FROM students;
```

This removes repeated values.

## 9. UPDATE data

```sql
UPDATE students
SET city = 'Nagpur'
WHERE name = 'Rahul';
```

This changes the city for Rahul.

## 10. DELETE data

```sql
DELETE FROM students WHERE id = 3;
```

This removes the row with id 3.

## 11. COUNT, SUM, AVG, MIN, MAX

```sql
SELECT COUNT(*) FROM students;
```

Counts total rows.

```sql
SELECT AVG(age) FROM students;
```

Gets average age.

```sql
SELECT SUM(age) FROM students;
```

Adds all ages.

```sql
SELECT MIN(age), MAX(age) FROM students;
```

Gets smallest and largest value.

## 12. GROUP BY

```sql
SELECT city, COUNT(*)
FROM students
GROUP BY city;
```

This groups students by city and counts how many are in each city.

```sql
SELECT city, AVG(age)
FROM students
GROUP BY city;
```

This gives the average age for each city.

## 13. HAVING

```sql
SELECT city, COUNT(*)
FROM students
GROUP BY city
HAVING COUNT(*) > 1;
```

`HAVING` is used after grouping to filter the grouped result.

## 14. JOINs

A join is used to combine rows from two tables.

### Inner join

```sql
SELECT s.name, c.course_name
FROM students s
JOIN enrollments e ON s.id = e.student_id
JOIN courses c ON c.course_id = e.course_id;
```

This shows only matching rows.

### Left join

```sql
SELECT s.name, c.course_name
FROM students s
LEFT JOIN enrollments e ON s.id = e.student_id
LEFT JOIN courses c ON c.course_id = e.course_id;
```

This shows all students, even if they do not have a course.

## 15. Constraints

Constraints are rules for the data.

- `PRIMARY KEY`: unique id for each row
- `FOREIGN KEY`: connection between tables
- `UNIQUE`: value must be different from others
- `NOT NULL`: field must have a value
- `CHECK`: value must match a condition
- `DEFAULT`: default value when not given

Example:

```sql
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(50) NOT NULL,
    credits INT CHECK (credits > 0)
);
```

## 16. Foreign key example

```sql
CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

This connects students with courses.

## 17. NULL values

`NULL` means no value or unknown value.

```sql
SELECT * FROM students WHERE city IS NULL;
```

```sql
SELECT * FROM students WHERE city IS NOT NULL;
```

## 18. Transactions

A transaction is a set of SQL commands that are executed together.

```sql
BEGIN;
UPDATE students SET city = 'Pune' WHERE id = 1;
UPDATE students SET city = 'Delhi' WHERE id = 2;
COMMIT;
```

If something is wrong, you can use `ROLLBACK`.

## 19. Common PostgreSQL data types

- `INT` for integer values
- `VARCHAR(n)` for text with max length
- `TEXT` for long text
- `BOOLEAN` for true/false
- `DATE` for dates
- `TIMESTAMP` for date and time
- `SERIAL` for auto-incrementing number

## 21. Very common SQL commands

```sql
CREATE TABLE
INSERT INTO
SELECT
UPDATE
DELETE
WHERE
ORDER BY
GROUP BY
JOIN
COUNT
AVG
SUM
MIN
MAX
```

## 