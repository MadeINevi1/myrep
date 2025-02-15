from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app import app  # Импортируем экземпляр Flask-приложения
from app.views import (  # Импортируем функции из views.py
    register, login as login_view, logout as logout_view,
    home, make_reservation, reservations, cancel_reservation_view,
    make_delivery_order, orders, profile,
    restaurant_reservations, add_dish,
    pending_orders, update_order_status_view
)

# ------------------------- Главная страница -------------------------
@app.route("/")
def index():
    """Главная страница приложения."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('base.html')

# ------------------------- Аутентификация -------------------------
@app.route("/register", methods=["GET", "POST"])
def register_route():
    """Маршрут для регистрации."""
    return register()

@app.route("/login", methods=["GET", "POST"])
def login_route():
    """Маршрут для входа в систему."""
    return login_view()

@app.route("/logout")
@login_required
def logout_route():
    """Маршрут для выхода из системы."""
    return logout_view()

# ------------------------- Клиентские функции -------------------------
@app.route("/home")
@login_required
def home_route():
    """Маршрут для главной страницы клиента."""
    return home()

@app.route("/reservation", methods=["GET", "POST"])
@login_required
def reservation_route():
    """Маршрут для бронирования столика."""
    return make_reservation()

@app.route("/reservations")
@login_required
def reservations_route():
    """Маршрут для просмотра бронирований клиента."""
    return reservations()

@app.route("/cancel_reservation/<int:reservation_id>")
@login_required
def cancel_reservation_route(reservation_id):
    """Маршрут для отмены бронирования."""
    return cancel_reservation_view(reservation_id)

@app.route("/delivery_order", methods=["GET", "POST"])
@login_required
def delivery_order_route():
    """Маршрут для оформления заказа на доставку."""
    return make_delivery_order()

@app.route("/orders")
@login_required
def orders_route():
    """Маршрут для просмотра заказов клиента."""
    return orders()

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile_route():
    """Маршрут для редактирования профиля клиента."""
    return profile()

# ------------------------- Административные функции -------------------------
@app.route("/restaurant_reservations/<int:restaurant_id>")
@login_required
def restaurant_reservations_route(restaurant_id):
    """Маршрут для просмотра бронирований ресторана администратором."""
    return restaurant_reservations(restaurant_id)

@app.route("/add_dish", methods=["GET", "POST"])
@login_required
def add_dish_route():
    """Маршрут для добавления блюда в меню ресторана администратором."""
    return add_dish()

# ------------------------- Функции оператора доставки -------------------------
@app.route("/pending_orders")
@login_required
def pending_orders_route():
    """Маршрут для просмотра ожидающих заказов оператором доставки."""
    return pending_orders()

@app.route("/update_order_status/<int:order_id>", methods=["GET", "POST"])
@login_required
def update_order_status_route(order_id):
    """Маршрут для обновления статуса заказа оператором доставки."""
    return update_order_status_view(order_id)