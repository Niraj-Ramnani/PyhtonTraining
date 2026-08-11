DROP FUNCTION IF EXISTS register_user(VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR);
DROP FUNCTION IF EXISTS place_order(INT, INT, JSONB, VARCHAR);
DROP FUNCTION IF EXISTS cancel_order(INT, INT);
DROP FUNCTION IF EXISTS update_restaurant(INT, VARCHAR, TEXT, VARCHAR, BOOLEAN);
DROP FUNCTION IF EXISTS update_food_price(INT, NUMERIC);


CREATE OR REPLACE FUNCTION register_user(
    p_name VARCHAR,
    p_email VARCHAR,
    p_password_hash VARCHAR,
    p_role_name VARCHAR DEFAULT 'customer',
    p_phone VARCHAR DEFAULT NULL
)
RETURNS TABLE(user_id INT, name VARCHAR, email VARCHAR, role_name VARCHAR)
LANGUAGE plpgsql
AS $$
DECLARE
    v_role_id INT;
BEGIN
    SELECT role_id INTO v_role_id
    FROM roles
    WHERE role_name = p_role_name;

    IF v_role_id IS NULL THEN
        RAISE EXCEPTION 'Role not found';
    END IF;

    RETURN QUERY
    INSERT INTO users(role_id, name, email, password_hash, phone)
    VALUES(v_role_id, p_name, LOWER(p_email), p_password_hash, p_phone)
    RETURNING users.user_id, users.name, users.email, p_role_name;
END;
$$;


CREATE OR REPLACE FUNCTION place_order(
    p_user_id INT,
    p_restaurant_id INT,
    p_items JSONB,
    p_payment_method VARCHAR DEFAULT 'upi'
)
RETURNS JSONB
LANGUAGE plpgsql
AS $$
DECLARE
    v_order_id INT;
    v_total NUMERIC(10,2) := 0;
    v_item JSONB;
    v_food_id INT;
    v_quantity INT;
    v_price NUMERIC(10,2);
BEGIN
    IF jsonb_array_length(p_items) = 0 THEN
        RAISE EXCEPTION 'Order must contain items';
    END IF;

    FOR v_item IN SELECT * FROM jsonb_array_elements(p_items)
    LOOP
        v_food_id := (v_item->>'food_item_id')::INT;
        v_quantity := (v_item->>'quantity')::INT;

        SELECT price INTO v_price
        FROM food_items
        WHERE food_item_id = v_food_id
        AND restaurant_id = p_restaurant_id
        AND is_available = TRUE;

        IF v_price IS NULL OR v_quantity <= 0 THEN
            RAISE EXCEPTION 'Invalid food item or quantity';
        END IF;

        v_total := v_total + (v_price * v_quantity);
    END LOOP;

    INSERT INTO orders(user_id, restaurant_id, total_amount)
    VALUES(p_user_id, p_restaurant_id, v_total)
    RETURNING order_id INTO v_order_id;

    FOR v_item IN SELECT * FROM jsonb_array_elements(p_items)
    LOOP
        v_food_id := (v_item->>'food_item_id')::INT;
        v_quantity := (v_item->>'quantity')::INT;

        SELECT price INTO v_price
        FROM food_items
        WHERE food_item_id = v_food_id;

        INSERT INTO order_items(
            order_id, food_item_id, quantity, unit_price, subtotal
        )
        VALUES(
            v_order_id,
            v_food_id,
            v_quantity,
            v_price,
            v_price * v_quantity
        );
    END LOOP;

    INSERT INTO payments(
        order_id, amount, payment_method, payment_status
    )
    VALUES(
        v_order_id, v_total, p_payment_method, 'successful'
    );

    RETURN jsonb_build_object(
        'order_id', v_order_id,
        'total_amount', v_total,
        'status', 'placed',
        'payment_status', 'successful'
    );
END;
$$;


CREATE OR REPLACE FUNCTION cancel_order(
    p_order_id INT,
    p_user_id INT
)
RETURNS JSONB
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE orders
    SET status = 'cancelled'
    WHERE order_id = p_order_id
    AND user_id = p_user_id
    AND status NOT IN ('delivered', 'cancelled');

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Order cannot be cancelled';
    END IF;

    UPDATE payments
    SET payment_status = 'refunded'
    WHERE order_id = p_order_id;

    RETURN jsonb_build_object(
        'order_id', p_order_id,
        'status', 'cancelled'
    );
END;
$$;


CREATE OR REPLACE FUNCTION update_restaurant(
    p_restaurant_id INT,
    p_name VARCHAR DEFAULT NULL,
    p_address TEXT DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL,
    p_is_active BOOLEAN DEFAULT NULL
)
RETURNS restaurants
LANGUAGE plpgsql
AS $$
DECLARE
    r restaurants;
BEGIN
    UPDATE restaurants
    SET name = COALESCE(p_name, name),
        address = COALESCE(p_address, address),
        phone = COALESCE(p_phone, phone),
        is_active = COALESCE(p_is_active, is_active)
    WHERE restaurant_id = p_restaurant_id
    RETURNING * INTO r;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Restaurant not found';
    END IF;

    RETURN r;
END;
$$;


CREATE OR REPLACE FUNCTION update_food_price(
    p_food_item_id INT,
    p_new_price NUMERIC
)
RETURNS food_items
LANGUAGE plpgsql
AS $$
DECLARE
    f food_items;
BEGIN
    IF p_new_price < 0 THEN
        RAISE EXCEPTION 'Price cannot be negative';
    END IF;

    UPDATE food_items
    SET price = p_new_price
    WHERE food_item_id = p_food_item_id
    RETURNING * INTO f;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Food item not found';
    END IF;

    RETURN f;
END;
$$;