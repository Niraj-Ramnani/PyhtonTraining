CREATE TABLE IF NOT EXISTS Roles (
    role_id     SERIAL PRIMARY KEY,
    role_name   TEXT NOT NULL UNIQUE CHECK (role_name IN ('customer', 'admin'))
);

CREATE TABLE IF NOT EXISTS Users (
    user_id         SERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    password_hash   TEXT NOT NULL,
    phone           TEXT,
    role_id         INTEGER NOT NULL DEFAULT 1 REFERENCES Roles(role_id),
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Restaurants (
    restaurant_id   SERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    address         TEXT NOT NULL,
    phone           TEXT,
    rating          DOUBLE PRECISION NOT NULL DEFAULT 0 CHECK (rating >= 0 AND rating <= 5),
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Categories (
    category_id     SERIAL PRIMARY KEY,
    category_name   TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Food_Items (
    food_item_id    SERIAL PRIMARY KEY,
    restaurant_id   INTEGER NOT NULL REFERENCES Restaurants(restaurant_id) ON DELETE CASCADE,
    category_id     INTEGER NOT NULL REFERENCES Categories(category_id),
    name            TEXT NOT NULL,
    price           DOUBLE PRECISION NOT NULL CHECK (price > 0),
    is_available    INTEGER NOT NULL DEFAULT 1 CHECK (is_available IN (0, 1)),
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Orders (
    order_id        SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES Users(user_id),
    restaurant_id   INTEGER NOT NULL REFERENCES Restaurants(restaurant_id),
    order_status    TEXT NOT NULL DEFAULT 'pending'
                    CHECK (order_status IN ('pending', 'confirmed', 'delivered', 'cancelled')),
    total_amount    DOUBLE PRECISION NOT NULL CHECK (total_amount >= 0),
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Order_Items (
    order_item_id   SERIAL PRIMARY KEY,
    order_id        INTEGER NOT NULL REFERENCES Orders(order_id) ON DELETE CASCADE,
    food_item_id    INTEGER NOT NULL REFERENCES Food_Items(food_item_id),
    quantity        INTEGER NOT NULL CHECK (quantity > 0),
    price_at_order  DOUBLE PRECISION NOT NULL CHECK (price_at_order >= 0)
);

CREATE TABLE IF NOT EXISTS Payments (
    payment_id      SERIAL PRIMARY KEY,
    order_id        INTEGER NOT NULL UNIQUE REFERENCES Orders(order_id) ON DELETE CASCADE,
    amount          DOUBLE PRECISION NOT NULL CHECK (amount >= 0),
    payment_method  TEXT NOT NULL CHECK (payment_method IN ('cash', 'card', 'upi')),
    payment_status  TEXT NOT NULL DEFAULT 'pending'
                    CHECK (payment_status IN ('pending', 'completed', 'failed')),
    paid_at         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Roles (role_id, role_name) VALUES (1, 'customer') ON CONFLICT (role_id) DO NOTHING;
INSERT INTO Roles (role_id, role_name) VALUES (2, 'admin') ON CONFLICT (role_id) DO NOTHING;
