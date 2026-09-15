from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Demo</title>
</head>
<body>
    <h2>WebSocket Practice</h2>
    <input id="message" placeholder="Type a message" />
    <button onclick="sendMessage()">Send</button>
    <div id="output"></div>

    <script>
        const socket = new WebSocket("ws://localhost:8000/ws");

        socket.onopen = function () {
            document.getElementById("output").innerHTML += "Connected<br>";
        };

        socket.onmessage = function (event) {
            document.getElementById("output").innerHTML += event.data + "<br>";
        };

        function sendMessage() {
            const input = document.getElementById("message");
            const value = input.value;
            socket.send(value);
            input.value = "";
        }
    </script>
</body>
</html>
"""


@app.get("/")
async def home():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Welcome to the WebSocket server")

    while True:
        message = await websocket.receive_text()
        reply = f"Server received: {message}"
        await websocket.send_text(reply)
