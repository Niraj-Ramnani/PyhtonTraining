"""
Day 3 – Inheritance, Polymorphism & Abstraction
1. Extend the Library Management System with PrintedBook, EBook and AudioBook classes.
2. Demonstrate inheritance from the Book class.
3. Implement borrow_duration() using polymorphism.
4. Create an abstract class LibraryItem with abstract methods issue_item() and return_item().

"""



from abc import ABC, abstractmethod


class LibraryItem(ABC):

    @abstractmethod
    def issue_item(self):
        # Issue the library items
        pass

    @abstractmethod
    def return_item(self):
        # Return the library items
        pass


class Book(LibraryItem):

    def __init__(self, book_id, title):
        self.book_id = book_id
        self.title = title
        self.__available = True


    def get_availability(self):
        return self.__available

    def set_availability(self, status):

        self.__available = status


    def issue_item(self):
        
        if self.get_availability():
            self.set_availability(False)
            print(f"\n'{self.title}' has been issued.")
        else:
            print("\nBook is already issued.")

    def return_item(self):
  
        self.set_availability(True)
        print(f"\n'{self.title}' has been returned.")



    def borrow_duration(self):

        return 14


    def __str__(self):
        status = (
            "Available"
            if self.get_availability()
            else "Issued"
        )

        return (
            f"Book ID : {self.book_id}\n"
            f"Title    : {self.title}\n"
            f"Status   : {status}"
        )

    def __repr__(self):
        return (
            f"Book({self.book_id}, "
            f"'{self.title}')"
        )

    def __eq__(self, other):
        if not isinstance(other, Book):
            return False

        return self.book_id == other.book_id



class PrintedBook(Book):

    def borrow_duration(self):
        return 21


class EBook(Book):

    def borrow_duration(self):
        return 30


class AudioBook(Book):
    

    def borrow_duration(self):
        return 15



class Member:
    

    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):


        if book.get_availability():

            book.issue_item()

            self.borrowed_books.append(book)

            print(
                f"Borrow Duration: "
                f"{book.borrow_duration()} days"
            )

        else:
            print("Book is unavailable.")

    def return_book(self, book):

        if book in self.borrowed_books:

            book.return_item()

            self.borrowed_books.remove(book)

        else:

            print("Book not borrowed.")

    def display_books(self):

        if not self.borrowed_books:

            print("\nNo borrowed books.\n")

            return

        print("\nBorrowed Books\n")

        for book in self.borrowed_books:

            print(book)

      




class Library:

    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def display_books(self):

        if not self.books:

            print("Library is empty.")

            return

        print("\nLibrary Books\n")

        for book in self.books:

            print(book)



    def find_book(self, book_id):

        for book in self.books:

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

            print("\n---Library Menu ---")
            print("1. Add Printed Book")
            print("2. Add EBook")
            print("3. Add AudioBook")
            print("4. Display Books")
            print("5. Borrow Book")
            print("6. Return Book")
            print("7. Display Borrowed Books")
            print("8. Exit")

            choice = input("Enter choice: ")

            if choice == "1":

                book_id = int(input("Book ID: "))
                title = input("Title: ")

                library.add_book(
                    PrintedBook(book_id, title)
                )

                print("Printed Book Added.")

            elif choice == "2":

                book_id = int(input("Book ID: "))
                title = input("Title: ")

                library.add_book(
                    EBook(book_id, title)
                )

                print("EBook Added.")

            elif choice == "3":

                book_id = int(input("Book ID: "))
                title = input("Title: ")

                library.add_book(
                    AudioBook(book_id, title)
                )

                print("AudioBook Added.")

            elif choice == "4":

                library.display_books()

            elif choice == "5":

                book_id = int(
                    input("Enter Book ID: ")
                )

                book = library.find_book(book_id)

                if book:

                    member.borrow_book(book)

                else:

                    print("Book not found.")

            elif choice == "6":

                book_id = int(
                    input("Enter Book ID: ")
                )

                book = library.find_book(book_id)

                if book:

                    member.return_book(book)

                else:

                    print("Book not found.")

            elif choice == "7":

                member.display_books()

            elif choice == "8":

                print("Program Executed ")

                break

            else:

                print("Invalid Choice.")

        except ValueError as error:

            print("Value Error:", error)

        except Exception as error:

            print("Unexpected Error:", error)


if __name__ == "__main__":
    main()