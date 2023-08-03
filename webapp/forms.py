from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    HiddenField,
)
from wtforms.validators import DataRequired


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
