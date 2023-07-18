from flask_wtf import FlaskForm
from webapp.model import User, RECIPE_CATEGORIES, PRODUCT_CATEGORIES, UNITS
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    FloatField,
    SelectField,
    HiddenField,
    IntegerField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    NumberRange,
    Optional,
    ValidationError,
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
        "Запомнить меня", render_kw={"class": "form-check-input"}
    )
    submit = SubmitField("Войти", render_kw={"class": "btn btn-primary w-100 py-2"})


class AddIngredientForm(FlaskForm):
    product = StringField(
        "Название ингредиента",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    category = SelectField(
        "Категория продукта",
        choices=list(PRODUCT_CATEGORIES.keys()),
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    quantity = FloatField(
        "Количество",
        validators=[
            NumberRange(min=0),
            DataRequired(),
        ],
        render_kw={"class": "form-control"},
    )
    unit = SelectField(
        "Единица измерения",
        choices=UNITS,
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    add = SubmitField(
        "Добавить", render_kw={"class": "btn btn-outline-primary w-100 py-2"}
    )


class AddRecipeForm(FlaskForm):
    name = StringField(
        "Название рецепта",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    category = SelectField(
        "Категория рецепта",
        choices=list(RECIPE_CATEGORIES.keys()),
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    description = StringField(
        "Текст рецепта",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    preparation_time = StringField(
        "Время на подготовку, мин",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    cooking_time = StringField(
        "Время на приготовление, мин",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    create = SubmitField(
        "Создать рецепт и перейти к добавлению ингредиентов",
        render_kw={"class": "btn btn-success w-100 py-2"},
    )


class CreateListForm(FlaskForm):
    name = StringField(
        "Название списка",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    submit = SubmitField("Создать", render_kw={"class": "btn btn-primary"})


class RenameElement(FlaskForm):
    new_value = StringField(
        "Новое название",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )

    element_id = HiddenField(
        "element_id",
        validators=[DataRequired()],
        render_kw={"id": "element_id"},
    )

    submit = SubmitField("Переименовать", render_kw={"class": "btn btn-primary"})


class AddShoppingItem(FlaskForm):
    name = StringField(
        "Название продукта",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "id": "new_item_name"},
    )

    quantity = FloatField(
        "Количество",
        validators=[Optional(), NumberRange(min=0)],
        default=0,
        render_kw={"class": "form-control"},
    )

    unit = SelectField(
        "Единица измерения",
        choices=UNITS,
        validators=[DataRequired()],
        render_kw={"class": "form-select"},
    )

    submit = SubmitField("Добавить", render_kw={"class": "btn btn-primary"})


class EditQuantityOfShoppingItemForm(FlaskForm):
    new_value = FloatField(
        "Количество",
        validators=[Optional(), NumberRange(min=0)],
        render_kw={"class": "form-control"},
    )

    element_id = HiddenField(
        "element_id",
        validators=[DataRequired()],
        render_kw={"id": "element_id"},
    )

    submit = SubmitField("Изменить", render_kw={"class": "btn btn-primary"})


class ChooseListForm(FlaskForm):
    name = SelectField(
        "Добавить продукты из рецепта в список покупок",
        validators=[DataRequired()],
        coerce=str,
        render_kw={"class": "form-control"},
    )
    portions = IntegerField(
        "Количество порций",
        validators=[DataRequired(), NumberRange(min=1)],
        default=1,
        render_kw={"class": "form-control"},
    )
    submit = SubmitField("Добавить", render_kw={"class": "btn btn-primary"})
