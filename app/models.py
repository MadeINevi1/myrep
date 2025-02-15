from datetime import datetime
from app.db import get_db_connection, close_db_connection

class User:
    def __init__(self, id, username, role, full_name=None, contact_phone=None, email=None):
        self.id = id
        self.username = username
        self.role = role
        self.full_name = full_name
        self.contact_phone = contact_phone
        self.email = email

    # ------------------------- Методы для клиента -------------------------

    def get_reservations(self):
        """Получить все бронирования клиента."""
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT r.reservation_id, res.name AS restaurant, r.reservation_date, r.reservation_time, r.guests_count 
                FROM reservations r
                JOIN restaurants res ON r.restaurant_id = res.restaurant_id
                WHERE r.client_id = %s
            """, (self.id,))
            reservations = cur.fetchall()
            close_db_connection(conn)
            return reservations
        return []

    def get_orders(self):
        """Получить все заказы клиента."""
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT o.order_id, r.name AS restaurant, o.order_date, o.delivery_address, o.status 
                FROM delivery_orders o
                JOIN restaurants r ON o.restaurant_id = r.restaurant_id
                WHERE o.client_id = %s
            """, (self.id,))
            orders = cur.fetchall()
            close_db_connection(conn)
            return orders
        return []

    def create_reservation(self, restaurant_id, reservation_date, reservation_time, guests_count):
        """Создать бронирование столика."""
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""
                    INSERT INTO reservations (client_id, restaurant_id, reservation_date, reservation_time, guests_count) 
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING reservation_id;
                """, (self.id, restaurant_id, reservation_date, reservation_time, guests_count))
                reservation_id = cur.fetchone()[0]
                conn.commit()
                return reservation_id
            except Exception as e:
                print(f"Ошибка при создании бронирования: {e}")
                conn.rollback()
                return None
            finally:
                close_db_connection(conn)
        return None

    def cancel_reservation(self, reservation_id):
        """Отменить бронирование."""
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""
                    UPDATE reservations 
                    SET status = 'canceled' 
                    WHERE reservation_id = %s AND client_id = %s;
                """, (reservation_id, self.id))
                conn.commit()
                return True
            except Exception as e:
                print(f"Ошибка при отмене бронирования: {e}")
                conn.rollback()
                return False
            finally:
                close_db_connection(conn)
        return False

    # ------------------------- Методы для администратора ресторана -------------------------

    def get_restaurant_reservations(self, restaurant_id):
        """Получить все бронирования для ресторана."""
        if self.role != 'admin':
            return []
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT r.reservation_id, c.full_name, r.reservation_date, r.reservation_time, r.guests_count 
                FROM reservations r
                JOIN clients c ON r.client_id = c.client_id
                WHERE r.restaurant_id = %s
            """, (restaurant_id,))
            reservations = cur.fetchall()
            close_db_connection(conn)
            return reservations
        return []

    def add_dish_to_menu(self, restaurant_id, name, description, price):
        """Добавить блюдо в меню ресторана."""
        if self.role != 'admin':
            return None
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""
                    INSERT INTO dishes (name, description, price) 
                    VALUES (%s, %s, %s)
                    RETURNING dish_id;
                """, (name, description, price))
                dish_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO menu_availability (restaurant_id, dish_id) 
                    VALUES (%s, %s);
                """, (restaurant_id, dish_id))
                conn.commit()
                return dish_id
            except Exception as e:
                print(f"Ошибка при добавлении блюда: {e}")
                conn.rollback()
                return None
            finally:
                close_db_connection(conn)
        return None

    # ------------------------- Методы для оператора доставки -------------------------

    def get_pending_orders(self):
        """Получить все заказы, ожидающие доставки."""
        if self.role != 'delivery_operator':
            return []
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT o.order_id, r.name AS restaurant, c.full_name, o.delivery_address, o.status 
                FROM delivery_orders o
                JOIN restaurants r ON o.restaurant_id = r.restaurant_id
                JOIN clients c ON o.client_id = c.client_id
                WHERE o.status IN ('processing', 'in_delivery');
            """)
            orders = cur.fetchall()
            close_db_connection(conn)
            return orders
        return []

    def update_order_status(self, order_id, status):
        """Обновить статус заказа."""
        if self.role != 'delivery_operator':
            return False
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""
                    UPDATE delivery_orders 
                    SET status = %s 
                    WHERE order_id = %s;
                """, (status, order_id))
                conn.commit()
                return True
            except Exception as e:
                print(f"Ошибка при обновлении статуса заказа: {e}")
                conn.rollback()
                return False
            finally:
                close_db_connection(conn)
        return False

# ------------------------- Вспомогательные функции -------------------------

def get_user_by_id(user_id):
    """Получить пользователя по ID."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT u.user_id, u.username, u.role, c.full_name, c.contact_phone, c.email 
            FROM users u
            LEFT JOIN clients c ON u.user_id = c.client_id
            WHERE u.user_id = %s
        """, (user_id,))
        user_data = cur.fetchone()
        close_db_connection(conn)

        if user_data:
            return User(
                id=user_data[0],
                username=user_data[1],
                role=user_data[2],
                full_name=user_data[3],
                contact_phone=user_data[4],
                email=user_data[5]
            )
    return None

def get_user_by_username(username):
    """Получить пользователя по имени пользователя."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT u.user_id, u.username, u.role, c.full_name, c.contact_phone, c.email 
            FROM users u
            LEFT JOIN clients c ON u.user_id = c.client_id
            WHERE u.username = %s
        """, (username,))
        user_data = cur.fetchone()
        close_db_connection(conn)

        if user_data:
            return User(
                id=user_data[0],
                username=user_data[1],
                role=user_data[2],
                full_name=user_data[3],
                contact_phone=user_data[4],
                email=user_data[5]
            )
    return None