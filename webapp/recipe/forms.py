from flask_wtf import FlaskForm
from webapp.db import UNITS
from webapp.recipe.models import RECIPE_CATEGORIES, PRODUCT_CATEGORIES, CUISINES, DIETS
from wtforms import (
    StringField,
    SubmitField,
    FloatField,
    SelectField,
)
from wtforms.validators import (
    DataRequired,
    NumberRange,
)


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
    cooking_time = StringField(
        "Время на приготовление, мин",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    create = SubmitField(
        "Создать рецепт и перейти к добавлению ингредиентов",
        render_kw={"class": "btn btn-success w-100 py-2"},
    )


class FindRecipeForm(FlaskForm):
    name = StringField(
        "Название рецепта",
        render_kw={"class": "form-control"},
    )
    category = SelectField(
        "Категория рецепта",
        choices=list(RECIPE_CATEGORIES.keys()),
        render_kw={"class": "form-control"},
    )

    cuisine = SelectField(
        "Кухня",
        choices=list(CUISINES.keys()),
        render_kw={"class": "form-control"},
    )

    diet = SelectField(
        "Диета",
        choices=list(DIETS.keys()),
        render_kw={"class": "form-control"},
    )

    search = SubmitField(
        "Найти рецепты",
        render_kw={"class": "btn btn-primary"},
    )
