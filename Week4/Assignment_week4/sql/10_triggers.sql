-- Q13: Database Triggers


CREATE OR REPLACE FUNCTION fn_update_restaurant_revenue()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_restaurant_id INT;
BEGIN
    IF NEW.payment_status = 'successful'
       AND (
           TG_OP = 'INSERT'
           OR OLD.payment_status IS DISTINCT FROM 'successful'
       ) THEN

        SELECT restaurant_id
        INTO v_restaurant_id
        FROM orders
        WHERE order_id = NEW.order_id;

        UPDATE restaurants
        SET revenue = revenue + NEW.amount
        WHERE restaurant_id = v_restaurant_id;
    END IF;

    -- Reverse revenue when a successful payment is refunded.
    IF TG_OP = 'UPDATE'
       AND OLD.payment_status = 'successful'
       AND NEW.payment_status = 'refunded' THEN

        SELECT restaurant_id
        INTO v_restaurant_id
        FROM orders
        WHERE order_id = NEW.order_id;

        UPDATE restaurants
        SET revenue = GREATEST(revenue - OLD.amount, 0)
        WHERE restaurant_id = v_restaurant_id;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_payment_revenue ON payments;

CREATE TRIGGER trg_payment_revenue
AFTER INSERT OR UPDATE OF payment_status ON payments
FOR EACH ROW
EXECUTE FUNCTION fn_update_restaurant_revenue();



CREATE OR REPLACE FUNCTION fn_reduce_inventory()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE food_items
    SET inventory = inventory - NEW.quantity
    WHERE food_item_id = NEW.food_item_id
      AND inventory >= NEW.quantity;

    IF NOT FOUND THEN
        RAISE EXCEPTION
            'Insufficient inventory for food item %',
            NEW.food_item_id;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_reduce_inventory ON order_items;

CREATE TRIGGER trg_reduce_inventory
AFTER INSERT ON order_items
FOR EACH ROW
EXECUTE FUNCTION fn_reduce_inventory();




CREATE OR REPLACE FUNCTION fn_prevent_pending_restaurant_delete()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM orders
        WHERE restaurant_id = OLD.restaurant_id
          AND status IN (
              'placed',
              'confirmed',
              'preparing',
              'out_for_delivery'
          )
    ) THEN
        RAISE EXCEPTION
            'Restaurant % cannot be deleted because it has pending orders',
            OLD.restaurant_id;
    END IF;

    RETURN OLD;
END;
$$;

DROP TRIGGER IF EXISTS trg_prevent_pending_restaurant_delete
ON restaurants;

CREATE TRIGGER trg_prevent_pending_restaurant_delete
BEFORE DELETE ON restaurants
FOR EACH ROW
EXECUTE FUNCTION fn_prevent_pending_restaurant_delete();



CREATE OR REPLACE FUNCTION fn_audit_deleted_food_item()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO food_item_audit (
        food_item_id,
        food_item_name,
        deleted_at,
        deleted_by
    )
    VALUES (
        OLD.food_item_id,
        OLD.name,
        CURRENT_TIMESTAMP,
        CURRENT_USER
    );

    RETURN OLD;
END;
$$;

DROP TRIGGER IF EXISTS trg_audit_deleted_food_item
ON food_items;

CREATE TRIGGER trg_audit_deleted_food_item
AFTER DELETE ON food_items
FOR EACH ROW
EXECUTE FUNCTION fn_audit_deleted_food_item();
