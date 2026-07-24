from abc import ABC, abstractmethod


class LibraryItem(ABC):
    total_items = 0

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self._issued = False
        LibraryItem.total_items += 1

    @property
    def issued(self):
        return self._issued

    @issued.setter
    def issued(self, value):
        if isinstance(value, bool):
            self._issued = value

    @abstractmethod
    def category(self):
        pass

    def __str__(self):
        status = "Issued" if self.issued else "Available"
        return f"{self.title} by {self.author} ({status})"

    @classmethod
    def item_count(cls):
        return cls.total_items

    @staticmethod
    def library_name():
        return "City Library"


class Book(LibraryItem):
    def category(self):
        return "Book"


class Magazine(LibraryItem):
    def category(self):
        return "Magazine"


class Member:
    def __init__(self, name):
        self.name = name
        self.borrowed = []

    def borrow(self, item):
        if item.issued:
            print(f"{item.title} is already issued.")
            return
        item.issued = True
        self.borrowed.append(item)
        print(f"{self.name} borrowed {item.title}")

    def return_item(self, item):
        if item in self.borrowed:
            item.issued = False
            self.borrowed.remove(item)
            print(f"{self.name} returned {item.title}")

    def show_items(self):
        if not self.borrowed:
            print(f"{self.name} has no borrowed items.")
            return
        print(f"\nItems with {self.name}:")
        for item in self.borrowed:
            print("-", item)


class Library:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def display(self):
        print("\nLibrary Collection")
        for item in self.items:
            print(item, "-", item.category())


library = Library()

book1 = Book("Atomic Habits", "James Clear")
book2 = Book("Python Crash Course", "Eric Matthes")
mag1 = Magazine("National Geographic", "NG Team")

library.add_item(book1)
library.add_item(book2)
library.add_item(mag1)

member = Member("Rahul")

library.display()

member.borrow(book1)
member.borrow(mag1)

member.show_items()

library.display()

member.return_item(book1)

print()
print("Library:", LibraryItem.library_name())
print("Total Items:", LibraryItem.item_count())