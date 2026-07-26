from models.movie import Movie
from models.customer import Customer, VIPCustomer
from models.booking import Booking, SeatIterator
from utils.booking_generator import booking_id_generator
from utils.copy_demo import backup
from exceptions import SeatUnavailableError


def main():

    movie_name = input("Enter Movie Name: ")
    total_seats = int(input("Enter Total Available Seats: "))

    movie = Movie(movie_name, total_seats)

    booking = Booking()

    generator = booking_id_generator()

 
    seats = []

    for i in range(1, total_seats + 1):
        seats.append(f"A{i}")

    print("\nAvailable Seats:")

    for seat in SeatIterator(seats):
        print(seat)

    while True:

        print("\n--- Movie Ticket Booking System ---")
        print("1. Book Ticket")
        print("2. Show Backups")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":

            name = input("Enter Customer Name: ")

            customer_type = input(
                "Enter Customer Type (Normal/VIP): "
            ).lower()

            if customer_type == "vip":
                customer = VIPCustomer(name)
            else:
                customer = Customer(name)

            try:
                booking.book(
                    next(generator),
                    customer,
                    movie
                )

                print(
                    f"Remaining Seats: {movie.get_seats()}"
                )

            except SeatUnavailableError as error:
                print(error)

        elif choice == "2":

            backup(booking.bookings)

        elif choice == "3":

            print("Program Executed ")
            break

        else:

            print("Invalid Choice.")


if __name__ == "__main__":
    main()