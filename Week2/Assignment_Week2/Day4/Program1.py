# 1. Create a custom iterator that iterates through the months of a year.
class MonthIterator:
    

    def __init__(self):
        self.months = [
            "January", "February", "March",
            "April", "May", "June",
            "July", "August", "September",
            "October", "November", "December"
        ]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.months):
            month = self.months[self.index]
            self.index += 1
            return month

        raise StopIteration


def main():
    iterator = MonthIterator()

    print("Months of the Year:\n")

    for month in iterator:
        print(month)


if __name__ == "__main__":
    main()