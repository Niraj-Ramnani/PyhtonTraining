SELECT u.user_id, u.name, u.email, SUM(o.total_amount) AS total_spent
FROM Users u
JOIN Orders o ON o.user_id = u.user_id
GROUP BY u.user_id, u.name, u.email
HAVING SUM(o.total_amount) = (
    SELECT MAX(customer_total)
    FROM (
        SELECT SUM(total_amount) AS customer_total
        FROM Orders
        GROUP BY user_id
    ) sub
);

SELECT f.food_item_id, f.name, f.restaurant_id
FROM Food_Items f
WHERE f.food_item_id NOT IN (
    SELECT DISTINCT food_item_id FROM Order_Items
);

SELECT r.restaurant_id, r.name, COUNT(o.order_id) AS total_orders
FROM Restaurants r
JOIN Orders o ON o.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_id, r.name
HAVING COUNT(o.order_id) > (
    SELECT AVG(order_count)
    FROM (
        SELECT COUNT(order_id) AS order_count
        FROM Orders
        GROUP BY restaurant_id
    ) sub
);

SELECT f.restaurant_id, f.food_item_id, f.name, f.price
FROM Food_Items f
WHERE f.price = (
    SELECT MAX(f2.price)
    FROM Food_Items f2
    WHERE f2.restaurant_id = f.restaurant_id
);

SELECT u.user_id, u.name, COUNT(o.order_id) AS order_count
FROM Users u
JOIN Orders o ON o.user_id = u.user_id
GROUP BY u.user_id, u.name
HAVING COUNT(o.order_id) > 5;
