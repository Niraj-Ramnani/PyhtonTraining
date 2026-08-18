# Day 1 — REST APIs with Python

Today we’ll cover:

1. REST architecture recap
2. Synchronous vs asynchronous APIs
3. Creating an API **without Flask/FastAPI**
4. Understanding HTTP requests and responses
5. Building a small REST API using Python's built-in `http.server`

## What is a REST API?

**REST = Representational State Transfer**

REST is an **architectural style** for designing network-based applications.

Important point:

> REST is not a programming language, library, or framework.

It is a set of principles for designing APIs.

## **Client-Server Architecture**

Client-server architecture is a computing model in which multiple clients (users or devices) interact with a centralized server to access data, resources, or services.

In this model, the **client** initiates requests (like fetching data or performing an action), while the **server** handles those requests, manages resources, and responds accordingly, often serving multiple clients at the same time.

<img src="https://substackcdn.com/image/fetch/$s_!F636!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa29b682c-cff6-4ed3-a085-4347eb020b06_1906x1150.png" width="693" />**Key Components:**

- **Client**: The client is typically a device or application that initiates a request to the server. This could be a web browser, a mobile app, or a desktop application.

- **Server**: The server is a powerful computer or software application that processes requests from clients, manages resources, and delivers the requested services or data.

- **Network**: The communication medium (usually the internet) that allows clients and servers to exchange data.

## HTTP and HTTP methods

GET → used to retieve data

POST → used to create a new resource

PUT → update exsisting resource

PATCH → for partial updates

DELETE → used to delete a resource

## Rest Principles

- **Client-Server Separation:** The UI (frontend) and data storage (backend) are completely independent.
- **Statelessness:** The server does not store session state. Every request must contain all information needed to process it.
- **Cacheability:** Responses must state whether they can be cached to save bandwidth and speed up requests.
- **Uniform Interface:** A consistent, predictable API design using standard URIs (nouns like `/users`) and standard HTTP verbs (`GET`, `POST`, `DELETE`).
- **Layered System:** The architecture can include proxies, load balancers, or security layers without the client knowing or caring.
- **Code on Demand (Optional):** Servers can send executable code (like JavaScript) to the client when necessary.

HTTP is a Protocol (The Tool) and REST is an Architectural Style (The Guide)

## Server Codes

2xx → Success

3xx → Redirection

4xx → Client error

5xx → Server error

### 200 — OK

Request succeeded.

```
200 OK
```

---

### 201 — Created

New resource successfully created.

```
201 Created
```

Typically used with POST.

---

### 204 — No Content

Request succeeded but there is no response body.

Commonly used for DELETE.

---

### 400 — Bad Request

Client sent invalid data.

```
400 Bad Request
```

Example:

```
"email": "invalid"
```

}

---

### 401 — Unauthorized

Authentication is missing or invalid.

```
401 Unauthorized
```

---

### 403 — Forbidden

User is authenticated but doesn't have permission.

```
403 Forbidden
```

---

### 404 — Not Found

Resource doesn't exist.

```
404 Not Found
```

---

### 500 — Internal Server Error

### A simple http request contains

contains:

HTTP methods

URL/Path

Headers

Body (optional)

## Synchronous and Asynchronous API

Synchronous = one operation waits for another operation to finish.

Asynchronous = an operation can wait for I/O  ( Database,Network ,HTTP API ,File system ) without blocking other work.

## Create REST API Without Frameworks

- `HTTPServer`**:** The server manager. It opens a network door on your machine, waits for incoming visitors (clients), and passes each request to your handler.
- `BaseHTTPRequestHandler`**:** The blueprint for handling traffic. It gives you ready-made tools to read incoming requests and write back status codes, headers, and responses.
- `do_GET`**:** The method triggered specifically when someone sends an HTTP **GET** request (like visiting the URL in a browser or fetching data).
- `self.send_response(200)`**:** The status signal. `200` is HTTP shorthand for "Everything is OK and request succeeded."
- `self.send_header(...)`**:** The metadata label. `"Content-Type", "application/json"` informs the client that the incoming data is formatted as JSON, not plain text or HTML.
- `self.end_headers()`**:** The divider line. In the HTTP standard, headers and body must be separated by an empty line; this function puts that separator in place.
- `server.serve_forever()`**:** The infinite loop. It keeps the Python script continuously alive and waiting for requests instead of finishing and closing immediately.

## Flask / FastApi makes this manual implementaion easier 

# Previous review questions 

### Q1 creating user using post 

```
from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "user1", "email": "user1@example.com"}
]

@app.route('/create-user', methods=['GET'])
def create_user_via_get():
    name = request.args.get('name')
    email = request.args.get('email')

    if not name or not email:
        return jsonify({"error": "Both 'name' and 'email' query parameters are required"}), 400

    new_user = {
        "id": len(users) + 1,
        "name": name,
        "email": email
    }
    users.append(new_user)

    return jsonify({
        "message": "User created successfully (via GET)",
        "user": new_user
    }), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**this violates REST / HTTP Standards**

`GET` requests must be **safe** (read-only) and produce no side effects on server data. Using `GET` to mutate state breaks caching proxies, pre-fetching crawlers, and browser history behavior (e.g., reloading the page or browser link pre-fetching could inadvertently create duplicate users).

### Q2 <span style="color: rgb(31, 31, 31);">what are idompetent api</span>

An **idempotent API** is one where making the **exact same request multiple times produces the identical server state** as making it once.

No matter how many times you repeat the call, the end result on the server does not change after the first successful execution.

- **Idempotent (**`GET`**,** `PUT`**,** `DELETE`**):**

  - `DELETE /users/5` <span>$\\rightarrow$</span> User 5 is deleted. Call it 10 more times <span>$\\rightarrow$</span> User 5 remains deleted.

  - `PUT /users/5` (setting `name = "Alex"`) <span>$\\rightarrow$</span> Call it 10 times <span>$\\rightarrow$</span> Name stays `"Alex"`.

- **Not Idempotent (**`POST`**,** `PATCH`**\*):**

  - `POST /users` (with data `{"name": "Alex"}`) <span>$\\rightarrow$</span> Call it 5 times <span>$\\rightarrow$</span> Creates 5 separate user records.

### Q3 what is new qurery method 

<span>The </span>`QUERY`<span> method is a newly standardized HTTP method designed to solve a long-standing limitation in web APIs: **how to perform complex, read-only data queries using a request body without breaking HTTP semantics.**</span>

### The Problem It Solves

Until now, developers were caught in an awkward trade-off when fetching filtered data:

- **Using** `GET`**:** `GET`<span> is **safe** and **idempotent**, but sending large, complex query filters via URL query parameters (</span>`/search?filter1=a&filter2=b...`<span>) runs into URL length limits (often \~2,000–8,000 characters)</span>

- **Using** `POST`**:** Developers frequently resorted to `POST /search` so they could send complex query bodies (like JSON filters or GraphQL). <span>However, </span>`POST`<span> is **not safe**, **not idempotent**, and **not cacheable** </span>

### Q4 What is SOAP

**SOAP (Simple Object Access Protocol)** is an official set of strict rules for exchanging data between two computer programs using **XML**.

Think of SOAP like sending a legal document in a sealed, registered envelope: it has strict formatting rules, high security, and requires a verified signature on both ends.

- **What it does:** It lets different software systems communicate reliably, even if one is written in Java and the other in C# or Python.

- **Format:** It only uses **XML** wrapped in a structured "envelope" (`<Envelope>`, `<Header>`, `<Body>`).

- **Strict Contract:** It uses a blueprint file (called a **WSDL**) that defines exactly what functions and data types are allowed. If the request doesn't match the contract 100%, it gets rejected immediately.

**SOAP does not compete with HTTP—it runs on top of it.**

- **HTTP is the Transport Vehicle:** It moves raw bytes, headers, and files across the network.

- **SOAP is the Strict Package inside the Vehicle:** It defines a standardized, sealed XML container (the "Envelope") carrying the actual message instructions.