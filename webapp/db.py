from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy(engine_options={"pool_pre_ping": True})
ma = Marshmallow()

UNITS = [
    "г",
    "мл",
    "шт.",
    "л",
    "кг",
    "ст. ложка",
    "ч. ложка",
    "стакан",
    "по вкусу",
    "зубчик",
    "веточка",
]


class ProjectSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    value = db.Column(db.Text, nullable=False)
