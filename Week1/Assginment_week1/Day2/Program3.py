try:
    students = {}
    n = int(input("Enter number of students "))
    for i in range (n):
        name = input("Enter name of the student")
        marks = int(input("Enter marks of student "))
        students[name] = marks

    filtered = {k: v for k, v in students.items() if k.startswith('A')}

    print(filtered)

except Exception as e:
    print("Error:", e)