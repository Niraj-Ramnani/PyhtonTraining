
INSERT INTO roles (role_name, description) VALUES
('admin', 'System administrator'),
('customer', 'Food ordering customer'),
('restaurant_owner', 'Restaurant owner')
ON CONFLICT (role_name) DO NOTHING;

INSERT INTO categories (name, description) VALUES
('Pizza', 'Pizza and Italian items'),
('Burgers', 'Burgers and sandwiches'),
('Indian', 'Indian meals'),
('Desserts', 'Sweet dishes'),
('Beverages', 'Hot and cold beverages')
ON CONFLICT (name) DO NOTHING;

INSERT INTO restaurants (name, address, phone) VALUES
('Spice Hub', 'MI Road, Jaipur', '9000000001'),
('Urban Tadka', 'Vaishali Nagar, Jaipur', '9000000002'),
('Pizza Point', 'C Scheme, Jaipur', '9000000003'),
('Burger House', 'Malviya Nagar, Jaipur', '9000000004'),
('Sweet Treats', 'Mansarovar, Jaipur', '9000000005')
ON CONFLICT (name) DO NOTHING;

INSERT INTO users (role_id, name, email, password_hash, phone)
SELECT r.role_id, x.name, x.email,
       'pbkdf2:sha256:600000$demoSalt12345678$RxKCifMCEso9WBl0TYgvsOagYWVEydOg9wviZueuJdM',
       x.phone
FROM roles r
CROSS JOIN (VALUES
    ('User 1','user1@example.com','9100000001'),
    ('User 2','user2@example.com','9100000002'),
    ('User 3','user3@example.com','9100000003'),
    ('User 4','user4@example.com','9100000004'),
    ('User 5','user5@example.com','9100000005'),
    ('User 6','user6@example.com','9100000006'),
    ('User 7','user7@example.com','9100000007'),
    ('User 8','user8@example.com','9100000008'),
    ('User 9','user9@example.com','9100000009'),
    ('User 10','user10@example.com','9100000010')
) AS x(name,email,phone)
WHERE r.role_name = 'customer'
ON CONFLICT (email) DO NOTHING;

INSERT INTO food_items
    (restaurant_id, category_id, name, description, price, inventory)
SELECT r.restaurant_id, c.category_id, x.name, x.description, x.price, x.inventory
FROM (VALUES
    ('Spice Hub','Indian','Paneer Thali','Full Indian thali',220,50),
    ('Spice Hub','Indian','Dal Tadka','Yellow dal',150,60),
    ('Spice Hub','Indian','Butter Paneer','Paneer curry',240,40),
    ('Spice Hub','Beverages','Lassi','Sweet lassi',80,80),
    ('Spice Hub','Desserts','Gulab Jamun','Two pieces',70,70),
    ('Spice Hub','Indian','Veg Biryani','Aromatic rice',190,50),
    ('Urban Tadka','Indian','Masala Dosa','South Indian dosa',160,60),
    ('Urban Tadka','Indian','Chole Bhature','Punjabi meal',180,50),
    ('Urban Tadka','Beverages','Masala Chaas','Spiced buttermilk',60,90),
    ('Urban Tadka','Desserts','Gajar Halwa','Carrot dessert',100,40),
    ('Urban Tadka','Indian','Rajma Rice','Rajma with rice',170,50),
    ('Urban Tadka','Indian','Veg Korma','Mixed vegetable curry',210,40),
    ('Pizza Point','Pizza','Margherita Pizza','Classic pizza',250,50),
    ('Pizza Point','Pizza','Farmhouse Pizza','Veggie pizza',320,45),
    ('Pizza Point','Pizza','Paneer Pizza','Paneer topping',340,45),
    ('Pizza Point','Pizza','Cheese Burst Pizza','Cheese filled crust',380,30),
    ('Pizza Point','Beverages','Cold Coffee','Chilled coffee',120,60),
    ('Pizza Point','Desserts','Brownie','Chocolate brownie',110,50),
    ('Burger House','Burgers','Veg Burger','Classic veg burger',140,60),
    ('Burger House','Burgers','Cheese Burger','Cheese veg burger',180,50),
    ('Burger House','Burgers','Double Patty Burger','Double patty',230,40),
    ('Burger House','Beverages','French Fries','Crispy fries',100,70),
    ('Burger House','Beverages','Iced Tea','Cold tea',90,70),
    ('Burger House','Desserts','Chocolate Shake','Chocolate shake',150,50),
    ('Sweet Treats','Desserts','Chocolate Cake','Slice of cake',160,40),
    ('Sweet Treats','Desserts','Red Velvet Cake','Red velvet slice',180,40),
    ('Sweet Treats','Desserts','Cheesecake','Classic cheesecake',220,35),
    ('Sweet Treats','Desserts','Donut','Glazed donut',80,80),
    ('Sweet Treats','Beverages','Cold Cocoa','Cold cocoa',130,60),
    ('Sweet Treats','Beverages','Mango Shake','Mango shake',150,60)
) AS x(restaurant_name,category_name,name,description,price,inventory)
JOIN restaurants r ON r.name = x.restaurant_name
JOIN categories c ON c.name = x.category_name
ON CONFLICT (restaurant_id, name) DO NOTHING;


DO $$
DECLARE
    i INT;
    uid INT;
    rid INT;
    fid INT;
    oid INT;
    amt NUMERIC(10,2);
BEGIN
    FOR i IN 1..20 LOOP
        uid := ((i - 1) % 10) + 1;
        rid := ((i - 1) % 5) + 1;

        SELECT food_item_id, price INTO fid, amt
        FROM food_items
        WHERE restaurant_id = rid
        ORDER BY food_item_id
        LIMIT 1;

        INSERT INTO orders (user_id, restaurant_id, total_amount, status)
        VALUES (uid, rid, amt, 'delivered')
        RETURNING order_id INTO oid;

        INSERT INTO order_items (order_id, food_item_id, quantity, unit_price, subtotal)
        VALUES (oid, fid, 1, amt, amt);

        INSERT INTO payments
            (order_id, amount, payment_method, payment_status, transaction_reference)
        VALUES
            (oid, amt, 'upi', 'successful', 'SEED-' || oid);
    END LOOP;
END $$;
