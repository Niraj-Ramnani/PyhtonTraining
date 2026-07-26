# 3. Create a closure that generates discount calculators.

def discount_calculator(discount):
    def calculate(price):
        return price - (price*discount/100)
    return calculate

def main():
    try:
        price = float(input("Enter product price : "))
        discount = float(input("Enter discound percentage : "))
        calculator = discount_calculator(discount)
        print("Final price after discount : ",calculator(price) )

    except Exception  as e:
        print("Error : " , e)

if __name__ == "__main__":
    main()