-- Q12: Sample Stored Function Calls
-- Run these after 01_schema.sql, 03_seed.sql, 08_transaction_function.sql
-- and 10_triggers.sql.

SELECT *
FROM register_user(
    'Function Test User',
    'function_test@example.com',
    'pbkdf2:sha256:600000$demoSalt12345678$RxKCifMCEso9WBl0TYgvsOagYWVEydOg9wviZueuJdM',
    'customer',
    '9199999999'
);

-- UpdateRestaurant
SELECT *
FROM update_restaurant(
    1,
    'Spice Hub Updated',
    'MI Road, Jaipur',
    '9000000001',
    TRUE
);

-- UpdateFoodPrice
SELECT *
FROM update_food_price(1, 225.00);

-- PlaceOrder
SELECT place_order(
    1,
    1,
    '[{"food_item_id": 1, "quantity": 1}]'::jsonb,
    'upi'
);
