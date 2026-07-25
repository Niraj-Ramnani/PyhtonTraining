"""

Day 2 – Classes, Objects & Encapsulation

1. Design a Library Management System using Book, Member and Library classes.
2. Store availability status as a private attribute and implement getter/setter methods.
3. Implement __str__(), __repr__() and __eq__() to represent and compare books.

"""


class Book:

    def __init__(self, book_id, title):
        self.book_id = book_id
        self.title = title
        self.__available = True

    def get_availability(self):
       
        return self.__available

    def set_availability(self, status):

        self.__available = status

    def __str__(self):
       
        status = "Available" if self.__available else "Not Available "

        return (
            f"Book ID : {self.book_id}\n"
            f"Title   : {self.title}\n"
            f"Status  : {status}"
        )

    def __repr__(self):

        return f"Book({self.book_id}, '{self.title}')"

    def __eq__(self, other):
       
        if not isinstance(other, Book):
            return False

        return self.book_id == other.book_id


class Member:
   

    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        
        if book.get_availability():
            book.set_availability(False)
            self.borrowed_books.append(book)
            print("Book added to your collection ")
        else:
            print("Book Not Available ")

    def return_book(self, book):
        
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.set_availability(True)
            print("Book Returned ")
        else:
            print("Book not in your collection ")

    def display_books(self):
        if not self.borrowed_books:
            print("No book in your collection ")
            return

        print("Books in your collection ")

        for book in self.borrowed_books:
            print(book)
            

class Library:

    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, book):
        self.books.append(book)

    def add_member(self, member):
        self.members.append(member)

    def display_books(self):
        
        if not self.books:
            print("\nLibrary is empty.\n")
            return

        print("\nLibrary Books\n")

        for book in self.books:
            print(book)

def find_book(library, book_id):

    for book in library.books:
        if book.book_id == book_id:
            return book

    return None
           





def main():


    library = Library()
    print("Creating a member for library : ")
    name = input("enter your name ")
    member = Member(1, name)
    library.add_member(member)

    while True:

        try:

            print("\n----Library Management ----\n")
            print("1. Add Book")
            print("2. Display Library Books")
            print("3. Borrow Book")
            print("4. Return Book")
            print("5. Display Borrowed Books")
            print("6. Compare Two Books (__eq__)")
            print("7. Display Book (__repr__)")
            print("8. Exit")

            choice = input("\nEnter your choice: ")

            if choice == "1":

                book_id = int(input("Enter Book ID: "))
                title = input("Enter Book Title: ")

                book = Book(book_id, title)
                library.add_book(book)

                print("\nBook added successfully.")

            elif choice == "2":

                library.display_books()

            elif choice == "3":

                book_id = int(input("Enter Book ID to borrow: "))

                book = find_book(library, book_id)

                if book:
                    member.borrow_book(book)
                else:
                    print("\nBook not found.")

            elif choice == "4":

                book_id = int(input("Enter Book ID to return: "))

                book = find_book(library, book_id)

                if book:
                    member.return_book(book)
                else:
                    print("\nBook not found.")

            elif choice == "5":

                member.display_books()

            elif choice == "6":

                id1 = int(input("Enter First Book ID: "))
                id2 = int(input("Enter Second Book ID: "))

                book1 = find_book(library, id1)
                book2 = find_book(library, id2)

        

                if book1 == book2:
                    print("\nBoth books are equal.")
                else:
                    print("\nBooks are different.")

        

            elif choice == "7":

                book_id = int(input("Enter Book ID: "))

                book = find_book(library, book_id)

                if book:
                    print("\nDeveloper Representation:")
                    print(repr(book))
                else:
                    print("\nBook not found.")

            elif choice == "8":

                print("Program Executed ")
                break

            else:
                print("\nInvalid choice.")

        except ValueError as error:
            print("\nValue Error:", error)

        except Exception as error:
            print("\nUnexpected Error:", error)


if __name__ == "__main__":
    main()