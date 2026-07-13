# Problem Statement: Create a Python program to calculate a student's average percentage, assign a grade, and display the examination result.

passing_marks = 40

def calculate_percentage(total_marks , subjects):
    return total_marks/subjects

def evaluate_student(name,mark1,mark2,mark3):
    total = mark1 + mark2 + mark3
    percentage = calculate_percentage(total,3)
    print("\n---Student Report---")
    print("Name : ", name)
    print("Total Marks :" , total)
    print("Percentage : " , round(percentage,2))

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 75:
        grade = "A"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 40:
        grade = "C"
    else:
        grade = "F"

    print("Grade : " , grade)

    if (percentage > passing_marks):
        print(" You cleared the examination.")
    else:
        print("Try again")

# main program

student_name = input("Enter Student name : ")
print("Enter marks out of 100")
mark1 = int(input("Enter mark for subject 1 : "))
mark2 = int(input("Enter mark for subject 2 : "))
mark3 = int(input("Enter mark for subject 3 : "))

evaluate_student(student_name , mark1 , mark2 , mark3)