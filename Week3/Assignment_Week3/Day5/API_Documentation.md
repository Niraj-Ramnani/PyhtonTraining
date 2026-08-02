# Online Food Ordering REST API Documentation

## Project Overview

This project is a REST API backend for an online food ordering system.

The API provides functionality for:

- User registration and login
- JWT based authentication
- User profile management
- Restaurant management
- Menu management
- Placing and viewing orders

## Base URL

```
http://127.0.0.1:5000
```

---

# Authentication APIs

## 1. Register User

Creates a new user account.

### Endpoint

```
POST /register
```

### Request Body

```json
{
    "name": "user1",
    "email": "user1@gmail.com",
    "password": "123456"
}
```

### Success Response

Status Code:

```
201 Created
```

Response:

```json
{
    "message": "User registered"
}
```

### Error Response

Status Code:

```
400 Bad Request
```

Example:

```json
{
    "error": "Email already exists"
}
```

---

## 2. User Login

Authenticates the user and returns a JWT token.

### Endpoint

```
POST /login
```

### Request Body

```json
{
    "email": "user1@gmail.com",
    "password": "123456"
}
```

### Success Response

Status Code:

```
200 OK
```

Response:

```json
{
    "token": "JWT_TOKEN"
}
```

### Error Response

Status Code:

```
401 Unauthorized
```

Response:

```json
{
    "error": "Invalid credentials"
}
```

---

# User Profile API

## 3. Get User Profile

Returns details of the currently logged-in user.

Authentication required.

### Endpoint

```
GET /profile
```

### Headers

```
Authorization: Bearer JWT_TOKEN
```

### Success Response

Status Code:

```
200 OK
```

Response:

```json
{
    "id": 1,
    "name": "user1",
    "email": "user1@gmail.com"
}
```

---

# Restaurant APIs

## 4. Add Restaurant

Adds a new restaurant.

Authentication required.

### Endpoint

```
POST /restaurants
```

### Headers

```
Authorization: Bearer JWT_TOKEN
```

### Request Body

```json
{
    "name": "Food Restaurant"
}
```

### Success Response

Status Code:

```
201 Created
```

Response:

```json
{
    "id": 1,
    "name": "Food Restaurant"
}
```

---

## 5. Get All Restaurants

Returns available restaurants.

### Endpoint

```
GET /restaurants
```

### Response

Status Code:

```
200 OK
```

Example:

```json
[
    {
        "id": 1,
        "name": "Food Restaurant"
    }
]
```

---

## 6. Get Restaurant By ID

Returns details of a specific restaurant.

### Endpoint

```
GET /restaurants/{id}
```

Example:

```
GET /restaurants/1
```

### Error Response

Status Code:

```
404 Not Found
```

```json
{
    "error": "Restaurant not found"
}
```

---

# Menu APIs

## 7. Add Menu Item

Adds a food item to a restaurant menu.

Authentication required.

### Endpoint

```
POST /menu
```

### Headers

```
Authorization: Bearer JWT_TOKEN
```

### Request Body

```json
{
    "restaurant_id": 1,
    "name": "Food Item 1",
    "price": 150
}
```

### Success Response

Status Code:

```
201 Created
```

Response:

```json
{
    "id": 1,
    "restaurant_id": 1,
    "name": "Food Item 1",
    "price": 150
}
```

### Validation

- Price should not be negative.
- Restaurant ID should be valid.

---

## 8. Get Restaurant Menu

Returns all menu items of a restaurant.

### Endpoint

```
GET /menu/{restaurant_id}
```

Example:

```
GET /menu/1
```

### Response

Status Code:

```
200 OK
```

Example:

```json
[
    {
        "id": 1,
        "restaurant_id": 1,
        "name": "Food Item 1",
        "price": 150
    }
]
```

---

# Order APIs

## 9. Create Order

Places a new food order.

Authentication required.

### Endpoint

```
POST /orders
```

### Headers

```
Authorization: Bearer JWT_TOKEN
```

### Request Body

```json
{
    "items": [1]
}
```

### Success Response

Status Code:

```
201 Created
```

Example:

```json
{
    "id": 1,
    "user_id": 1,
    "items": [1],
    "total": 150,
    "status": "placed"
}
```

---

## 10. Get User Orders

Returns orders placed by the logged-in user.

Authentication required.

### Endpoint

```
GET /orders
```

### Headers

```
Authorization: Bearer JWT_TOKEN
```

### Response

Status Code:

```
200 OK
```

---

## 11. Get Order By ID

Returns details of a specific order.

Authentication required.

### Endpoint

```
GET /orders/{id}
```

Example:

```
GET /orders/1
```

### Error Response

Status Code:

```
404 Not Found
```

```json
{
    "error": "Order not found"
}
```

---

# HTTP Status Codes Used

| Status Code | Description |
|------------|-------------|
| 200 | Request completed successfully |
| 201 | New resource created |
| 400 | Invalid request data |
| 401 | Authentication required or failed |
| 404 | Requested resource not found |

---

# Authentication Method

This API uses JWT (JSON Web Token) authentication.

For protected routes, send the token in the request header:

```
Authorization: Bearer JWT_TOKEN
```

---

# Validation Implemented

The API includes the following validations:

- Required fields validation
- Duplicate email checking
- Password hashing before storing
- JWT authentication for protected routes
- Negative price validation
- Invalid resource ID handling
- User-specific order access

---

# Tools Used

- Python
- Flask
- Flask-JWT-Extended
- Werkzeug Password Hashing
- Postman for API testing