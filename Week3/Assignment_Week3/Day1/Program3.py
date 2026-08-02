# 3. Generate student report from file using context managers only; calculate averages and handle missing files.
class StudentReport:

    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, "r")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

        if exc_type:
            print("Error:", exc_value)

        return False

try:

    with StudentReport("students.txt") as file:

        print("Student Report :")

        for line in file:

            data = line.strip().split(",")

            name = data[0]

            marks = list(map(int, data[1:]))

            average = sum(marks) / len(marks)

            print(f"{name} -> Average = {average:.2f}")

except FileNotFoundError:
    print("Student file not found.")