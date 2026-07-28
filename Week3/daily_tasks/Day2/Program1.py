class HttpRequest:
    def __init__(self, method, path, body=None):
        self.method = method.upper()
        self.path = path
        self.body = body


class HttpResponse:
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body


class Server:

    def __init__(self):
        self.users = {
            1: {"name": "Alice", "age": 21},
            2: {"name": "Bob", "age": 25},
        }

    def handle_request(self, request):

        # GET
        if request.method == "GET":

            if request.path == "/users":
                return HttpResponse(200, self.users)

        # POST
        elif request.method == "POST":

            user_id = max(self.users.keys()) + 1

            self.users[user_id] = request.body

            return HttpResponse(201, "User Created")

        # PUT
        elif request.method == "PUT":

            user_id = request.body["id"]

            if user_id in self.users:

                self.users[user_id] = {
                    "name": request.body["name"],
                    "age": request.body["age"]
                }

                return HttpResponse(200, "User Updated")

            return HttpResponse(404, "User Not Found")

        # PATCH
        elif request.method == "PATCH":

            user_id = request.body["id"]

            if user_id in self.users:

                self.users[user_id].update(request.body["data"])

                return HttpResponse(200, "User Patched")

            return HttpResponse(404, "User Not Found")

        # DELETE
        elif request.method == "DELETE":

            user_id = request.body["id"]

            if user_id in self.users:

                del self.users[user_id]

                return HttpResponse(200, "User Deleted")

            return HttpResponse(404, "User Not Found")

        return HttpResponse(400, "Bad Request")


server = Server()

while True:

    print("\n1.GET")
    print("2.POST")
    print("3.PUT")
    print("4.PATCH")
    print("5.DELETE")
    print("6.EXIT")

    choice = input("Choice : ")

    if choice == "6":
        break

    if choice == "1":

        request = HttpRequest("GET", "/users")

    elif choice == "2":

        name = input("Name : ")
        age = int(input("Age : "))

        request = HttpRequest(
            "POST",
            "/users",
            {"name": name, "age": age}
        )

    elif choice == "3":

        uid = int(input("User ID : "))
        name = input("New Name : ")
        age = int(input("New Age : "))

        request = HttpRequest(
            "PUT",
            "/users",
            {"id": uid, "name": name, "age": age}
        )

    elif choice == "4":

        uid = int(input("User ID : "))
        key = input("Field(name/age) : ")

        value = input("Value : ")

        if key == "age":
            value = int(value)

        request = HttpRequest(
            "PATCH",
            "/users",
            {
                "id": uid,
                "data": {key: value}
            }
        )

    elif choice == "5":

        uid = int(input("User ID : "))

        request = HttpRequest(
            "DELETE",
            "/users",
            {"id": uid}
        )

    else:
        continue

    response = server.handle_request(request)

    print(response.status_code)
    print(response.body)