from http.server import HTTPServer, BaseHTTPRequestHandler


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(b'{"message": "Hello from Python API"}')


server = HTTPServer(("localhost", 8000), MyHandler)

print("Server running on http://localhost:8000")

server.serve_forever()