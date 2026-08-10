EXPLAIN (ANALYZE, BUFFERS)
SELECT user_id, name, email
FROM users
WHERE email = 'user1@example.com';

EXPLAIN (ANALYZE, BUFFERS)
SELECT restaurant_id, name
FROM restaurants
WHERE name = 'Spice Hub';

EXPLAIN (ANALYZE, BUFFERS)
SELECT food_item_id, name, price
FROM food_items
WHERE restaurant_id = 1;

EXPLAIN (ANALYZE, BUFFERS)
SELECT order_id, total_amount, status, ordered_at
FROM orders
WHERE user_id = 1
ORDER BY ordered_at DESC;


CREATE INDEX IF NOT EXISTS idx_users_email
    ON users(email);

CREATE INDEX IF NOT EXISTS idx_restaurants_name
    ON restaurants(name);

CREATE INDEX IF NOT EXISTS idx_food_items_restaurant_id
    ON food_items(restaurant_id);

CREATE INDEX IF NOT EXISTS idx_orders_user_id_ordered_at
    ON orders(user_id, ordered_at DESC);

CREATE INDEX IF NOT EXISTS idx_orders_restaurant_id
    ON orders(restaurant_id);

CREATE INDEX IF NOT EXISTS idx_order_items_food_item_id
    ON order_items(food_item_id);

CREATE INDEX IF NOT EXISTS idx_payments_status
    ON payments(payment_status);

EXPLAIN (ANALYZE, BUFFERS)
SELECT user_id, name, email
FROM users
WHERE email = 'user1@example.com';

EXPLAIN (ANALYZE, BUFFERS)
SELECT restaurant_id, name
FROM restaurants
WHERE name = 'Spice Hub';

EXPLAIN (ANALYZE, BUFFERS)
SELECT food_item_id, name, price
FROM food_items
WHERE restaurant_id = 1;

EXPLAIN (ANALYZE, BUFFERS)
SELECT order_id, total_amount, status, ordered_at
FROM orders
WHERE user_id = 1
ORDER BY ordered_at DESC;