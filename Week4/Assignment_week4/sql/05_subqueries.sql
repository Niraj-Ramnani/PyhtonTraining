SELECT
    u.user_id,
    u.name,
    u.email,
    SUM(o.total_amount) AS total_spending
FROM users u
JOIN orders o ON o.user_id = u.user_id
GROUP BY u.user_id, u.name, u.email
HAVING SUM(o.total_amount) = (
    SELECT MAX(customer_total)
    FROM (
        SELECT SUM(total_amount) AS customer_total
        FROM orders
        GROUP BY user_id
    ) spending
);


SELECT
    f.food_item_id,
    f.name,
    f.restaurant_id,
    f.price
FROM food_items f
WHERE NOT EXISTS (
    SELECT 1
    FROM order_items oi
    WHERE oi.food_item_id = f.food_item_id
)
ORDER BY f.food_item_id;

SELECT
    r.restaurant_id,
    r.name,
    COUNT(o.order_id) AS total_orders
FROM restaurants r
LEFT JOIN orders o ON o.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_id, r.name
HAVING COUNT(o.order_id) > (
    SELECT AVG(order_count)
    FROM (
        SELECT COUNT(o2.order_id) AS order_count
        FROM restaurants r2
        LEFT JOIN orders o2
            ON o2.restaurant_id = r2.restaurant_id
        GROUP BY r2.restaurant_id
    ) restaurant_counts
)
ORDER BY total_orders DESC;


SELECT
    f.restaurant_id,
    f.food_item_id,
    f.name,
    f.price
FROM food_items f
WHERE f.price = (
    SELECT MAX(f2.price)
    FROM food_items f2
    WHERE f2.restaurant_id = f.restaurant_id
)
ORDER BY f.restaurant_id, f.food_item_id;

SELECT
    u.user_id,
    u.name,
    u.email,
    (
        SELECT COUNT(*)
        FROM orders o
        WHERE o.user_id = u.user_id
    ) AS order_count
FROM users u
WHERE (
    SELECT COUNT(*)
    FROM orders o
    WHERE o.user_id = u.user_id
) > 5
ORDER BY order_count DESC;
