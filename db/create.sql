DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS restaurant_admins;
DROP TABLE IF EXISTS dishes;
DROP TABLE IF EXISTS menu_availability;
DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS delivery_orders;
DROP TABLE IF EXISTS order_items;

-- Таблица пользователей (общая для всех ролей)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('client', 'admin', 'delivery_operator'))
);

-- Таблица клиентов (расширение users)
CREATE TABLE clients (
    client_id INT PRIMARY KEY REFERENCES users(user_id),
    full_name VARCHAR(100) NOT NULL,
    contact_phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    preferences TEXT
);

-- Таблица ресторанов
CREATE TABLE restaurants (
    restaurant_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    contact_phone VARCHAR(20) NOT NULL,
    working_hours TEXT NOT NULL,
    description TEXT
);

-- Таблица администраторов ресторанов (связь user + restaurant)
CREATE TABLE restaurant_admins (
    admin_id INT PRIMARY KEY REFERENCES users(user_id),
    restaurant_id INT REFERENCES restaurants(restaurant_id) ON DELETE SET NULL
);

-- Таблица блюд
CREATE TABLE dishes (
    dish_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10,2) NOT NULL CHECK (price > 0)
);

-- Таблица доступности блюд в ресторанах
CREATE TABLE menu_availability (
    restaurant_id INT REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    dish_id INT REFERENCES dishes(dish_id) ON DELETE CASCADE,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (restaurant_id, dish_id)
);

-- Таблица бронирований
CREATE TABLE reservations (
    reservation_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clients(client_id) ON DELETE CASCADE,
    restaurant_id INT REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    reservation_date DATE NOT NULL,
    reservation_time TIME NOT NULL,
    guests_count INT NOT NULL CHECK (guests_count > 0),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'canceled'))
);

-- Таблица заказов на доставку
CREATE TABLE delivery_orders (
    order_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clients(client_id) ON DELETE CASCADE,
    restaurant_id INT REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    delivery_address TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'processing' CHECK (status IN ('processing', 'in_delivery', 'delivered', 'canceled'))
);

-- Таблица позиций в заказе
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES delivery_orders(order_id) ON DELETE CASCADE,
    dish_id INT REFERENCES dishes(dish_id) ON DELETE CASCADE,
    quantity INT NOT NULL CHECK (quantity > 0)
);