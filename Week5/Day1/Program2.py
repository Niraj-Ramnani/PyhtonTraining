from http.server import HTTPServer, BaseHTTPRequestHandler
import json


users = [
    {
        "id": 1,
        "name": "user1",
        "email": "user1@example.com"
    },
    {
        "id": 2,
        "name": "user2",
        "email": "user2@example.com"
    }
]


class UserHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):
        response = json.dumps(data).encode()

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)

    def do_GET(self):

        if self.path == "/users":
            self.send_json(200, users)
            return

        if self.path.startswith("/users/"):

            user_id = self.path.split("/")[-1]

            try:
                user_id = int(user_id)
            except ValueError:
                self.send_json(400, {
                    "error": "Invalid user ID"
                })
                return

            for user in users:
                if user["id"] == user_id:
                    self.send_json(200, user)
                    return

            self.send_json(404, {
                "error": "User not found"
            })
            return

        self.send_json(404, {
            "error": "Endpoint not found"
        })


server = HTTPServer(("localhost", 8000), UserHandler)

print("Server running on http://localhost:8000")

server.serve_forever()