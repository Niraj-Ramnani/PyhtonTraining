# API Documentation

Base URL: `http://127.0.0.1:5000`

## Authentication

### POST /register
```json
{
  "name": "Demo User",
  "email": "demo@example.com",
  "password": "Password@123",
  "phone": "9199999999"
}
```

### POST /login
```json
{
  "email": "demo@example.com",
  "password": "Password@123"
}
```

Use the returned token:
`Authorization: Bearer <token>`

## Profile

`GET /profile` — JWT required.

## Restaurants

- `GET /restaurants` — public
- `GET /restaurants/{id}` — public
- `POST /restaurants` — admin/restaurant_owner
- `PUT /restaurants/{id}` — admin/restaurant_owner
- `DELETE /restaurants/{id}` — admin

## Menu

- `GET /menu/{restaurant_id}` — public
- `POST /menu` — admin/restaurant_owner
- `PUT /menu/{food_item_id}` — admin/restaurant_owner
- `DELETE /menu/{food_item_id}` — admin/restaurant_owner

## Orders

`POST /orders`:
```json
{
  "restaurant_id": 1,
  "items": [
    {"food_item_id": 1, "quantity": 2}
  ],
  "payment_method": "upi"
}
```

Other endpoints:
- `GET /orders`
- `GET /orders/{id}`
- `PATCH /orders/{id}/cancel`

All order endpoints require JWT authentication.

## Status codes

- 200 OK
- 201 Created
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 409 Conflict
