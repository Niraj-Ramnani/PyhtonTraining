
SELECT
    f.food_item_id,
    f.name AS food_item_name,
    r.name AS restaurant_name,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.subtotal) AS sales_amount
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
JOIN food_items f ON f.food_item_id = oi.food_item_id
JOIN restaurants r ON r.restaurant_id = f.restaurant_id
WHERE o.status <> 'cancelled'
GROUP BY f.food_item_id, f.name, r.name
ORDER BY units_sold DESC, sales_amount DESC
LIMIT 10;


SELECT
    r.restaurant_id,
    r.name AS restaurant_name,
    DATE_TRUNC('month', p.paid_at)::date AS sales_month,
    SUM(p.amount) AS monthly_revenue
FROM payments p
JOIN orders o ON o.order_id = p.order_id
JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE p.payment_status = 'successful'
GROUP BY
    r.restaurant_id,
    r.name,
    DATE_TRUNC('month', p.paid_at)
ORDER BY sales_month, monthly_revenue DESC;

SELECT
    o.ordered_at::date AS order_date,
    COUNT(*) AS total_orders,
    COUNT(*) FILTER (WHERE o.status = 'cancelled') AS cancelled_orders,
    COUNT(*) FILTER (WHERE o.status <> 'cancelled') AS successful_orders,
    COALESCE(
        SUM(o.total_amount) FILTER (WHERE o.status <> 'cancelled'),
        0
    ) AS successful_order_value
FROM orders o
GROUP BY o.ordered_at::date
ORDER BY order_date;


SELECT
    u.user_id,
    u.name,
    u.email,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS total_spending
FROM users u
JOIN orders o ON o.user_id = u.user_id
WHERE o.status <> 'cancelled'
GROUP BY u.user_id, u.name, u.email
ORDER BY total_spending DESC
LIMIT 10;

SELECT
    r.restaurant_id,
    r.name AS restaurant_name,
    COUNT(o.order_id) AS order_count,
    ROUND(AVG(o.total_amount), 2) AS average_order_value
FROM restaurants r
LEFT JOIN orders o
    ON o.restaurant_id = r.restaurant_id
   AND o.status <> 'cancelled'
GROUP BY r.restaurant_id, r.name
ORDER BY average_order_value DESC NULLS LAST;
