def booking_id_generator():
    booking_id = 1000

    while True:
        yield booking_id
        booking_id += 1