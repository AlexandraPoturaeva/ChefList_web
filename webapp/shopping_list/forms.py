from flask_wtf import FlaskForm
from webapp.db import UNITS
from wtforms import (
    StringField,
    SubmitField,
    FloatField,
    SelectField,
    HiddenField,
    IntegerField,
)
from wtforms.validators import (
    DataRequired,
    NumberRange,
    Optional,
)


class CreateListForm(FlaskForm):
    name = StringField(
        "Название списка",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    submit = SubmitField("Создать", render_kw={"class": "btn btn-primary"})


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
        render_kw={"class": "form-control", "type": "number", "min": "0"},
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
    recipe_info = HiddenField(validators=[DataRequired()])
    portions = IntegerField(
        "Количество порций",
        validators=[DataRequired(), NumberRange(min=1)],
        default=1,
        render_kw={"class": "form-control"},
    )
    submit = SubmitField("Добавить", render_kw={"class": "btn btn-primary"})
