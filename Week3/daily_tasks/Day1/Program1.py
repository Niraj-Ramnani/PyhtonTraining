# Simulating Client-Server Communication 
""" 
Concept Covered
Client
Server
Request
Response
"""

class Server:
    def process_request(self, request):
        print("Request receieved ")
        if request == "GET_USER_NAME":
            return "username"
        elif request == "GET_USER_ID":
            return "userid"
        else:
            return "404 request not found "

class Client:
    def __init__(self , server ):
        self.server = server

    def send_request(self , request):
        print(f"Client : sending -> {request}")

        response = self.server.process_request(request)
        print(f"Server response -> {response}" )

server = Server()
client = Client(server)

client.send_request("GET_USER_NAME")
client.send_request("404")