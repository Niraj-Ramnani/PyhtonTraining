def divide():
    try:
        num1 = int(input("Enter value: "))
        num2 = int(input("Enter value: "))

        if num2 == 0:
            raise ZeroDivisionError("Can not divide with zero")

        result = num1 / num2

        filename = input("Enter file name: ")
        with open(filename, "w") as file:
            file.write(f"{num1} / {num2} = {result}\n")

    except ValueError:
        print("Error: Please enter valid integers.")

    except ZeroDivisionError as e:
        print("Error:", e)

    except FileNotFoundError:
        print("Error: File not found.")

    else:
        print("Result =", result)
        print("Result saved successfully.")

    finally:
        print("Operation completed")



divide()