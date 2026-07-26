# 1. Demonstrate assignment, shallow copy and deep copy using nested student records.
import copy


def display_records(title, records):
    print(f"\n{title}")

    for student in records:
        print(student)


def main():

    students = [
        {
            "name": "Student1",
            "marks": [85, 90, 95]
        },
        {
            "name": "Student2",
            "marks": [89, 80, 82]
        }
    ]

    # Assignment
    assigned_records = students

    # Shallow Copy
    shallow_records = copy.copy(students)

    # Deep Copy
    deep_records = copy.deepcopy(students)

    print("\nOriginal Records")
    display_records("Students", students)

    print("\nModifying Original Data")

    students[0]["marks"][0] = 100
    students[1]["name"] = "new student"

    display_records("Original", students)
    display_records("Assignment Copy", assigned_records)
    display_records("Shallow Copy", shallow_records)
    display_records("Deep Copy", deep_records)


if __name__ == "__main__":
    main()