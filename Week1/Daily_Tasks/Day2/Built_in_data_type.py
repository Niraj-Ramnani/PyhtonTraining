#-------Library Management System--------#

library = []


def add_book():
    book = {}
    book["id"] = int(input("Enter book ID : "))
    book["price"] = float(input("Enter book price "))
    book["available"] = True
    library.append(book)
    print("Book Added")



def display_book():
    if(len(library) == 0):
        print("No books available")
        return
    print("\n---Books in Library---\n")
    for book in library:
        print("Book Id : ", book["id"])
        print("Book Price : ", book["price"])
        print("Availability : ", book["available"])
        print()

def search_book():
    sid = int(input("Enter book id : "))
    for book in library:
        if book["id"] == sid:
            print("Book Found")
            print(book)
            return
    print("Book not found")

def issue_book():
    book_id = int(input("enter the book id : "))
    for book in library:
        if book["id"] == book_id:
            library.remove(book)
            print("Book Issued")
        else:
            print("Book not found")

#---Main Program---#

while True:
    print("\n---Library Management System---\n")
    print("1 : Add Book")
    print("2 : Display Books")
    print("3 : Search Book")
    print("4 : Issue Books")
    choice = int(input("enter a choice : "))
    if choice == 1:
        add_book()
    elif choice == 2:
        display_book()
    elif choice == 3:
        search_book()
    elif choice == 4:
        issue_book()
    else:
        print("Invalid choice")