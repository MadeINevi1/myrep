from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from app.forms import (
    RegistrationForm, LoginForm, ReservationForm, DeliveryOrderForm,
    EditProfileForm, AddDishForm, UpdateOrderStatusForm, SearchRestaurantForm
)
from app.models import (
    get_user_by_username, User  # Импортируем только необходимые компоненты
)

# ------------------------- Аутентификация -------------------------
def register():
    """Регистрация нового пользователя."""
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User.register_user(
            username=form.email.data,
            password=form.password.data,
            role='client',
            full_name=form.full_name.data,
            contact_phone=form.contact_phone.data,
            email=form.email.data
        )
        if new_user:
            flash('Вы успешно зарегистрировались!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Не удалось зарегистроваться. Попробуйте снова.', 'error')
    return render_template('register.html', form=form)


def login():
    """Авторизация пользователя."""
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Неверный email или пароль.', 'error')
    return render_template('login.html', form=form)


@login_required
def logout():
    """Выход из системы."""
    logout_user()
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('home'))


# ------------------------- Клиентские функции -------------------------
@login_required
def home():
    """Главная страница."""
    return render_template('home.html')


@login_required
def make_reservation():
    """Бронирование столика."""
    form = ReservationForm()
    if form.validate_on_submit():
        reservation_id = current_user.create_reservation(
            restaurant_id=form.restaurant.data,
            reservation_date=form.reservation_date.data,
            reservation_time=form.reservation_time.data,
            guests_count=form.guests_count.data
        )
        if reservation_id:
            flash('Столик успешно забронирован!', 'success')
            return redirect(url_for('reservations'))
        else:
            flash('Не удалось забронировать столик.', 'error')
    return render_template('reservation.html', form=form)


@login_required
def reservations():
    """Просмотр бронирований клиента."""
    reservations = current_user.get_reservations()
    return render_template('reservations.html', reservations=reservations)


@login_required
def cancel_reservation_view(reservation_id):
    """Отмена бронирования."""
    success = current_user.cancel_reservation(reservation_id)
    if success:
        flash('Бронирование успешно отменено.', 'success')
    else:
        flash('Не удалось отменить бронирование.', 'error')
    return redirect(url_for('reservations'))


@login_required
def make_delivery_order():
    """Оформление заказа на доставку."""
    form = DeliveryOrderForm()
    if form.validate_on_submit():
        # Здесь можно добавить логику создания заказа в базе данных
        flash('Заказ успешно оформлен!', 'success')
        return redirect(url_for('orders'))
    return render_template('delivery_order.html', form=form)


@login_required
def orders():
    """Просмотр заказов клиента."""
    orders = current_user.get_orders()
    return render_template('orders.html', orders=orders)


@login_required
def profile():
    """Редактирование профиля клиента."""
    form = EditProfileForm(obj=current_user)  # Заполнение формы текущими данными пользователя
    if form.validate_on_submit():
        # Здесь можно добавить логику обновления данных пользователя в базе данных
        flash('Профиль успешно обновлен!', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form)


# ------------------------- Административные функции -------------------------
@login_required
def restaurant_reservations(restaurant_id):
    """Просмотр бронирований ресторана администратором."""
    if current_user.role != 'admin':
        flash('У вас нет прав доступа к этой странице.', 'error')
        return redirect(url_for('home'))
    reservations = current_user.get_restaurant_reservations(restaurant_id)
    return render_template('restaurant_reservations.html', reservations=reservations)


@login_required
def add_dish():
    """Добавление блюда в меню ресторана администратором."""
    if current_user.role != 'admin':
        flash('У вас нет прав доступа к этой странице.', 'error')
        return redirect(url_for('home'))
    form = AddDishForm()
    if form.validate_on_submit():
        dish_id = current_user.add_dish_to_menu(
            restaurant_id=request.args.get('restaurant_id'),
            name=form.name.data,
            description=form.description.data,
            price=form.price.data
        )
        if dish_id:
            flash('Блюдо успешно добавлено!', 'success')
            return redirect(url_for('add_dish'))
        else:
            flash('Не удалось добавить блюдо.', 'error')
    return render_template('add_dish.html', form=form)


# ------------------------- Функции оператора доставки -------------------------
@login_required
def pending_orders():
    """Просмотр ожидающих заказов оператором доставки."""
    if current_user.role != 'delivery_operator':
        flash('У вас нет прав доступа к этой странице.', 'error')
        return redirect(url_for('home'))
    orders = current_user.get_pending_orders()
    return render_template('pending_orders.html', orders=orders)


@login_required
def update_order_status_view(order_id):
    """Обновление статуса заказа оператором доставки."""
    if current_user.role != 'delivery_operator':
        flash('У вас нет прав доступа к этой странице.', 'error')
        return redirect(url_for('home'))
    form = UpdateOrderStatusForm()
    if form.validate_on_submit():
        success = current_user.update_order_status(order_id, form.status.data)
        if success:
            flash('Статус заказа успешно обновлен!', 'success')
        else:
            flash('Не удалось обновить статус заказа.', 'error')
    return render_template('update_order_status.html', form=form, order_id=order_id)