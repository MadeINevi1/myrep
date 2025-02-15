from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, SelectField, FieldList, FormField, TextAreaField, SelectMultipleField, IntegerField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange

# ------------------------- Формы для клиентов -------------------------

class RegistrationForm(FlaskForm):
    """Форма регистрации клиента."""
    full_name = StringField('ФИО', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact_phone = StringField('Контактный телефон', validators=[DataRequired(), Length(min=10, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    """Форма авторизации."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class ReservationForm(FlaskForm):
    """Форма бронирования столика."""
    restaurant = SelectField('Ресторан', coerce=int, validators=[DataRequired()])
    reservation_date = DateField('Дата бронирования', validators=[DataRequired()])
    reservation_time = TimeField('Время бронирования', validators=[DataRequired()])
    guests_count = IntegerField('Количество гостей', validators=[DataRequired(), NumberRange(min=1, max=20)])
    submit = SubmitField('Забронировать')


class DeliveryOrderForm(FlaskForm):
    """Форма заказа на доставку."""
    restaurant = SelectField('Ресторан', coerce=int, validators=[DataRequired()])
    delivery_address = StringField('Адрес доставки', validators=[DataRequired()])
    dishes = SelectMultipleField('Выберите блюда', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Оформить заказ')


class EditProfileForm(FlaskForm):
    """Форма редактирования профиля клиента."""
    full_name = StringField('ФИО', validators=[DataRequired(), Length(min=2, max=100)])
    contact_phone = StringField('Контактный телефон', validators=[DataRequired(), Length(min=10, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Сохранить изменения')


# ------------------------- Формы для администратора ресторана -------------------------

class AddDishForm(FlaskForm):
    """Форма добавления блюда в меню."""
    name = StringField('Название блюда', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Описание', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Добавить блюдо')


class EditRestaurantForm(FlaskForm):
    """Форма редактирования информации о ресторане."""
    name = StringField('Название ресторана', validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField('Адрес', validators=[DataRequired()])
    contact_phone = StringField('Контактный телефон', validators=[DataRequired(), Length(min=10, max=20)])
    working_hours = StringField('Часы работы', validators=[DataRequired()])
    submit = SubmitField('Сохранить изменения')


# ------------------------- Формы для оператора доставки -------------------------

class UpdateOrderStatusForm(FlaskForm):
    """Форма обновления статуса заказа."""
    status = SelectField('Статус заказа', choices=[
        ('processing', 'В обработке'),
        ('in_delivery', 'В доставке'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен')
    ], validators=[DataRequired()])
    submit = SubmitField('Обновить статус')


# ------------------------- Общие формы -------------------------

class SearchRestaurantForm(FlaskForm):
    """Форма поиска ресторана."""
    name = StringField('Название ресторана', validators=[DataRequired()])
    submit = SubmitField('Найти')


class MessageForm(FlaskForm):
    """Форма отправки сообщения."""
    text = TextAreaField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class CommentForm(FlaskForm):
    """Форма добавления комментария."""
    text = TextAreaField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Отправить')