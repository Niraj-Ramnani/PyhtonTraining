class Student:
    count = 0

    def __init__(self):
        Student.count += 1

    @classmethod
    def total_students(cls):
        return cls.count

Student()
Student()
Student()

print(Student.total_students())