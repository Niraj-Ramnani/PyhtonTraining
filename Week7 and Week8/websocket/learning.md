# WebSocket Learning

## What is a WebSocket?
WebSocket is a way to keep a live connection between the client and server. It is useful when messages need to move quickly in both directions without reloading the page.

## How it works
- The client connects to a websocket route on the server.
- The server accepts the connection.
- After that, both sides can send messages continuously.
- This is different from HTTP, where the client usually sends one request and gets one response.

## Why use WebSocket?
Use WebSockets for:
- chat apps
- live notifications
- stock updates
- online dashboards

## FastAPI with WebSocket
FastAPI makes it easy to create a websocket route using the WebSocket class.

Basic flow:
1. Open a connection
2. Accept the connection
3. Receive messages from client
4. Send messages back to client
5. Close when done

## Simple example flow
A browser connects to the server.
The server sends a welcome message.
The browser sends a text message.
The server replies with the same text and a server message.

## Practice idea
Create a small app with:
- home page
- websocket route
- JavaScript client in the browser
- send and receive messages

## Run it
Use:
uvicorn main:app --reload

Then open the browser and connect to the local URL.
