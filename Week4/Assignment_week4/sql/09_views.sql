-- Q11: Database Views

DROP VIEW IF EXISTS restaurant_revenue_summary;
DROP VIEW IF EXISTS monthly_sales_summary;
DROP VIEW IF EXISTS top_selling_food_items;
DROP VIEW IF EXISTS active_restaurants;
DROP VIEW IF EXISTS customer_order_history;

CREATE VIEW customer_order_history AS
SELECT
    u.user_id,
    u.name AS customer_name,
    u.email,
    o.order_id,
    o.restaurant_id,
    r.name AS restaurant_name,
    oi.order_item_id,
    f.food_item_id,
    f.name AS food_item_name,
    oi.quantity,
    oi.unit_price,
    oi.subtotal,
    o.total_amount,
    o.status,
    p.payment_status,
    o.ordered_at
FROM users u
JOIN orders o ON o.user_id = u.user_id
JOIN restaurants r ON r.restaurant_id = o.restaurant_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN food_items f ON f.food_item_id = oi.food_item_id
LEFT JOIN payments p ON p.order_id = o.order_id;

CREATE VIEW active_restaurants AS
SELECT
    restaurant_id,
    name,
    address,
    phone,
    revenue,
    created_at
FROM restaurants
WHERE is_active = TRUE;


CREATE VIEW top_selling_food_items AS
SELECT
    f.food_item_id,
    f.name AS food_item_name,
    r.restaurant_id,
    r.name AS restaurant_name,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.subtotal) AS sales_amount
FROM food_items f
JOIN restaurants r ON r.restaurant_id = f.restaurant_id
JOIN order_items oi ON oi.food_item_id = f.food_item_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status <> 'cancelled'
GROUP BY
    f.food_item_id,
    f.name,
    r.restaurant_id,
    r.name;

CREATE VIEW monthly_sales_summary AS
SELECT
    DATE_TRUNC('month', p.paid_at)::date AS sales_month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(p.amount) AS total_sales
FROM payments p
JOIN orders o ON o.order_id = p.order_id
WHERE p.payment_status = 'successful'
GROUP BY DATE_TRUNC('month', p.paid_at);

CREATE VIEW restaurant_revenue_summary AS
SELECT
    r.restaurant_id,
    r.name AS restaurant_name,
    COUNT(DISTINCT o.order_id)
        FILTER (WHERE o.status <> 'cancelled') AS total_orders,
    COALESCE(
        SUM(p.amount) FILTER (WHERE p.payment_status = 'successful'),
        0
    ) AS payment_revenue,
    r.revenue AS stored_revenue
FROM restaurants r
LEFT JOIN orders o ON o.restaurant_id = r.restaurant_id
LEFT JOIN payments p ON p.order_id = o.order_id
GROUP BY r.restaurant_id, r.name, r.revenue;

SELECT * FROM customer_order_history ORDER BY ordered_at DESC;
SELECT * FROM active_restaurants ORDER BY restaurant_id;
SELECT * FROM top_selling_food_items ORDER BY units_sold DESC;
SELECT * FROM monthly_sales_summary ORDER BY sales_month;
SELECT * FROM restaurant_revenue_summary ORDER BY payment_revenue DESC;
