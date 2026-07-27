# Simulating an HTTP Request & Response
"""
Concept Covered
HTTP Request
HTTP Response
Status Codes
Headers
Body
"""
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

    users = []

    def handle_request(self, request):

        if request.method == "GET" and request.path == "/users":
            return HttpResponse(200, self.users)

        elif request.method == "POST" and request.path == "/users":

            self.users.append(request.body)

            return HttpResponse(
                201,
                f"{request.body} Added Successfully"
            )

        return HttpResponse(404, "Invalid Request")


server = Server()
path = input("Enter Path : ")
while(True):
    
    method = input("Enter Method get / post : ")

    body = None

    if method.upper() == "POST":
        body = input("Enter User Name : ")

    request = HttpRequest(method, path, body)

    response = server.handle_request(request)

    print("\nStatus :", response.status_code)
    print("Response :", response.body)

    print("\nCurrent Users :", server.users)