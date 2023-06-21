from flask_wtf import FlaskForm
from webapp.model import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    ValidationError,
    NumberRange,
)


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
    remember_me = BooleanField(
        "Запомнить меня", default=False, render_kw={"class": "form-check-input"}
    )
    submit = SubmitField("Войти", render_kw={"class": "btn btn-primary w-100 py-2"})


class AddIngredientForm(FlaskForm):
    product = StringField(
        "Название ингредиента",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    quantity = FloatField(
        "Количество",
        validators=[
            DataRequired(),
            NumberRange(min=0),
        ],
        render_kw={"class": "form-control"},
    )
    unit = StringField(
        "Единица измерения",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    add = SubmitField("Добавить", render_kw={"class": "btn btn-primary w-100 py-2"})


class AddRecipeForm(FlaskForm):
    name = StringField(
        "Название рецепта",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    category = StringField(
        "Категория рецепта",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    description = StringField(
        "Текст рецепта",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    preparation_time = StringField(
        "Время на подготовку",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    cooking_time = StringField(
        "Время на приготовление",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    create = SubmitField(
        "Создать рецепт", render_kw={"class": "btn btn-primary w-100 py-2"}
    )

    
class CreateListForm(FlaskForm):
    name = StringField('Название списка',
                       validators=[DataRequired()],
                       render_kw={"class": "form-control"})
    submit = SubmitField('Создать', render_kw={"class": "btn btn-primary"})

