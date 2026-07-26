from exceptions import SeatUnavailableError
from utils.logger import booking_logger


class SeatIterator:

    def __init__(self, seats):
        self.seats = seats
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):

        if self.index >= len(self.seats):
            raise StopIteration

        seat = self.seats[self.index]

        self.index += 1

        return seat


class Booking:

    def __init__(self):
        self.bookings = []

    @booking_logger
    def book(self, booking_id, customer, movie):

        if movie.get_seats() <= 0:
            raise SeatUnavailableError(
                "Seats are not available."
            )

        movie.book_ticket()

        self.bookings.append(
            {
                "Booking ID": booking_id,
                "Customer": customer.name,
                "Movie": movie.name,
                "Price": customer.ticket_price()
            }
        )

        print(self.bookings[-1])