from flask_wtf import FlaskForm
from webapp.model import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField(
        'Адрес электронной почты',
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"}
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    password2 = PasswordField(
        'Повторите пароль',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField('Зарегистрироваться', render_kw={"class": "btn btn-primary"})

    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError('пользователь с таким email уже существует')


class LoginForm(FlaskForm):
    email = StringField(
        'Адрес электронной почты',
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"})
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    remember_me = BooleanField('Запомнить меня', default=False, render_kw={"class": "form-check-input"})
    submit = SubmitField('Войти', render_kw={"class": "btn btn-primary w-100 py-2"})


class CreateListForm(FlaskForm):
    name = StringField('Название списка',
                       validators=[DataRequired()],
                       render_kw={"class": "form-control"})
    submit = SubmitField('Создать', render_kw={"class": "btn btn-primary"})


class AddShoppingItem(FlaskForm):
    name = StringField('Название продукта',
                       validators=[DataRequired()],
                       render_kw={"class": "form-control"})
    submit = SubmitField('Добавить', render_kw={"class": "btn btn-primary"})


class SelectShoppingItem(FlaskForm):
    select = BooleanField('Вычеркнуть', default=False, render_kw={"class": "form-check-input"})
