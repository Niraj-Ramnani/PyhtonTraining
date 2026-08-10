# Normalization to 3NF

## 1NF
Every column contains atomic values. An order does not contain a comma-separated list of food IDs; each ordered food is a separate `order_items` row.

## 2NF
Non-key attributes depend on the complete key of the row. `order_items` stores quantity, unit price and subtotal for one specific order-item record.

## 3NF
Non-key attributes do not depend on other non-key attributes:
- Role data is separated into `roles`.
- Category data is separated into `categories`.
- Restaurant data is separated into `restaurants`.
- Payment data is separated into `payments`.
- Order line data is separated into `order_items`.

This removes repeated data and reduces update, insertion and deletion anomalies.

`restaurants.revenue` is intentionally maintained as a derived operational value because the assignment explicitly requires a restaurant-sales/revenue trigger.
