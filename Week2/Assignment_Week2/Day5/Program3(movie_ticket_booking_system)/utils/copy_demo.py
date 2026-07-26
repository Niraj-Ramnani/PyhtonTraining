import copy


def backup(bookings):

    shallow = copy.copy(bookings)

    deep = copy.deepcopy(bookings)

    print("\nShallow Copy")
    print(shallow)

    print("\nDeep Copy")
    print(deep)