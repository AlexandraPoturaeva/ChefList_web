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
        choices=[("-1", "Категория")]
        + [(key, value[0]) for key, value in RECIPE_CATEGORIES.items()],
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
        choices=[("-1", "Категория")]
        + [(key, value[0]) for key, value in RECIPE_CATEGORIES.items()],
        render_kw={"class": "form-control"},
    )

    cuisine = SelectField(
        "Кухня",
        choices=[("-1", "Кухня")]
        + [(key, value[0]) for key, value in CUISINES.items()],
        render_kw={"class": "form-control"},
    )

    diet = SelectField(
        "Диета",
        choices=[("-1", "Диета")] + [(key, value[0]) for key, value in DIETS.items()],
        render_kw={"class": "form-control"},
    )

    search = SubmitField(
        "Найти рецепты",
        render_kw={"class": "btn btn-primary"},
    )

    def validate(self, extra_validators=None):
        if super().validate(extra_validators):
            if all(
                [
                    data == "-1"
                    for data in [
                        self.name.data,
                        self.category.data,
                        self.diet.data,
                        self.cuisine.data,
                    ]
                ]
            ):
                self.search.errors.append("Хотя бы одно поле должно быть заполнено")
                return False
            else:
                return True
