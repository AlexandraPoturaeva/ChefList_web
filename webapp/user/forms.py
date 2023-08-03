from flask_wtf import FlaskForm
from webapp.user.models import User
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    name = StringField(
        "Имя", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    email = StringField(
        "Адрес электронной почты",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"},
    )
    password = PasswordField(
        "Пароль", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    password2 = PasswordField(
        "Повторите пароль",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"class": "form-control"},
    )
    submit = SubmitField("Зарегистрироваться", render_kw={"class": "btn btn-primary"})

    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data.lower()).count()
        if users_count > 0:
            raise ValidationError("Пользователь с таким email уже существует")


class LoginForm(FlaskForm):
    email = StringField(
        "Адрес электронной почты",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"},
    )
    password = PasswordField(
        "Пароль", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    submit = SubmitField("Войти", render_kw={"class": "btn btn-primary w-100 py-2"})
