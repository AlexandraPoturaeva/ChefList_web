from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(engine_options={"pool_pre_ping": True})

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
