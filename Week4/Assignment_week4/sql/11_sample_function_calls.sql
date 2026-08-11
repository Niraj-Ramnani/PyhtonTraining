SELECT *
FROM register_user(
    'Function Test User',
    'function_test@example.com',
    'customer',
    '9199999999'
);

SELECT *
FROM update_restaurant(
    1,
    'Spice Hub Updated',
    'MI Road, Jaipur',
    '9000000001',
    TRUE
);

SELECT *
FROM update_food_price(1, 225.00);

SELECT place_order(
    1,
    1,
    '[{"food_item_id": 1, "quantity": 1}]'::jsonb,
    'upi'
);
