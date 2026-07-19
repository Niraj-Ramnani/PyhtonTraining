# 3. Write a script that filters a dictionary to include only key-value pairs where the key starts with the letter 'A.' (use comprehensions).
try:
    students = {}
    n = int(input("Enter number of students "))
    for i in range (n):
        name = input(f"Enter name of the student {i+1} : ")
        marks = int(input("Enter marks of student : "))
        students[name] = marks

    filtered = {k: v for k, v in students.items() if k.startswith('A')}
    print("Unfiltered Data : ")
    print(students)
    print("Filtered Data : ")
    print(filtered)

except Exception as e:
    print("Error:", e)