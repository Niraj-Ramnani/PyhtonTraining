SELECT
    r.restaurant_id,
    r.name AS restaurant_name,
    f.food_item_id,
    f.name AS food_item_name,
    f.price,
    f.is_available
FROM restaurants r
LEFT JOIN food_items f
    ON f.restaurant_id = r.restaurant_id
ORDER BY r.restaurant_id, f.food_item_id;


SELECT
    u.user_id,
    u.name AS customer_name,
    o.order_id,
    o.restaurant_id,
    o.total_amount,
    o.status,
    o.ordered_at
FROM users u
JOIN roles ro
    ON ro.role_id = u.role_id
LEFT JOIN orders o
    ON o.user_id = u.user_id
WHERE ro.role_name = 'customer'
ORDER BY u.user_id, o.ordered_at;


SELECT
    o.order_id,
    u.name AS customer_name,
    r.name AS restaurant_name,
    STRING_AGG(
        f.name || ' x ' || oi.quantity,
        ', ' ORDER BY f.name
    ) AS ordered_items,
    o.total_amount,
    COALESCE(p.payment_status, 'not_created') AS payment_status
FROM orders o
JOIN users u ON u.user_id = o.user_id
JOIN restaurants r ON r.restaurant_id = o.restaurant_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN food_items f ON f.food_item_id = oi.food_item_id
LEFT JOIN payments p ON p.order_id = o.order_id
GROUP BY
    o.order_id,
    u.name,
    r.name,
    o.total_amount,
    p.payment_status
ORDER BY o.order_id;


SELECT
    r.restaurant_id,
    r.name AS restaurant_name
FROM restaurants r
LEFT JOIN food_items f
    ON f.restaurant_id = r.restaurant_id
WHERE f.food_item_id IS NULL
ORDER BY r.restaurant_id;


SELECT
    f.food_item_id,
    f.name AS food_item_name,
    c.category_id,
    c.name AS category_name,
    f.price
FROM food_items f
JOIN categories c
    ON c.category_id = f.category_id
ORDER BY c.name, f.name;
