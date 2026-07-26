class Customer:

    def __init__(self, name):
        self.name = name

    def ticket_price(self):
        return 200


class VIPCustomer(Customer):

    def ticket_price(self):
        return 150