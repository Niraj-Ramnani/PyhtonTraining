from functools import wraps


def booking_logger(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        print("\nBooking Started")

        result = function(*args, **kwargs)

        print("Booking Successful.")

        return result

    return wrapper