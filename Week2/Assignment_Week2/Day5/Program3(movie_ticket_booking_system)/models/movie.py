from abc import ABC, abstractmethod


class BookingItem(ABC):

    @abstractmethod
    def book_ticket(self):
        pass

    @abstractmethod
    def cancel_ticket(self):
        pass


class Movie(BookingItem):

    def __init__(self, name, seats):
        self.name = name
        self.__available_seats = seats

    def get_seats(self):
        return self.__available_seats

    def set_seats(self, seats):
        self.__available_seats = seats

    def book_ticket(self):
        self.__available_seats -= 1

    def cancel_ticket(self):
        self.__available_seats += 1