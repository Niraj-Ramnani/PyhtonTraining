# 2. Create DatabaseConnection context manager simulating connect/disconnect, insert/retrieve and exception handling.
class DatabaseConnection:

    def __init__(self):
        self.database = []

    def __enter__(self):
        print("Database Connected")
        return self

    def insert(self, data):
        self.database.append(data)
        print(f"Inserted: {data}")

    def retrieve(self):
        return self.database

    def __exit__(self, exc_type, exc_value, traceback):

        if exc_type:
            print("Database Error:", exc_value)

        print("Database Disconnected")

        return False

try:

    with DatabaseConnection() as db:
        n = int(input("Enter number of entries you want to insert : "))
        for i in range(n):
            db.insert(input("Enter name for database : "))

        print("Records:")
        print(db.retrieve())


except Exception as e:
    print("Caught:", e)