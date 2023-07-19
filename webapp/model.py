from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(engine_options={"pool_pre_ping": True})

PRODUCT_CATEGORIES = {
    "Хлебобулочные изделия": "burlywood",
    "Кондитерские товары": "goldenrod",
    "Молочная продукция": "seashell",
    "Мясные товары": "brown",
    "Колбасная продукция": "salmon",
    "Рыба и морепродукты": "steelblue",
    "Овощи-фрукты": "limegreen",
    "Бакалея": "hotpink",
    "Напитки": "magenta",
}

RECIPE_CATEGORIES = {
    "Первые блюда": "firebrick",
    "Вторые блюда": "darkgoldenrod",
    "Закуски": "lightskyblue",
    "Салаты": "springgreen",
    "Соусы, кремы": "peachpuff",
    "Напитки": "orangered",
    "Десерты": "darkorange",
    "Выпечка": "lemonchiffon",
    "Торты": "mistyrose",
    "Блины и оладьи": "burlywood",
}

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


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    shopping_lists = db.relationship("ShoppingList", backref="user", lazy=True)

    def __init__(self, email, name):
        self.email = email
        self.name = name

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return (
            f"User {self.id} "
            f"\nemail: {self.email} "
            f"\nname: {self.name}"
            f"\ncreated_at {self.created_at}"
        )


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, index=True, unique=True)
    category = db.Column(db.Text)

    def __repr__(self):
        return f"<Product: {self.name}, category: {self.category}>"


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category = db.Column(db.Text)
    description = db.Column(db.Text)
    preparation_time = db.Column(db.Text)
    cooking_time = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ingredients = db.relationship(
        "Ingredient", backref="recipe", lazy=True, cascade="all, delete"
    )

    def __repr__(self):
        return f"<Recipe: {self.name} by user with id {self.user_id}>"


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.Text)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))
    product = db.relationship("Product")

    def __str__(self):
        product_name = db.session.query(Product).get(self.product_id).name
        return f"{product_name}, {self.quantity} {self.unit}"

    def __repr__(self):
        return f"<Ingredient: {self.product_id} for recipe {self.recipe_id}>"


class ShoppingList(db.Model):
    __tablename__ = "shopping_list"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    shopping_items = db.relationship(
        "ShoppingItem", backref="shopping_list", lazy=True, cascade="all, delete"
    )
    public_id = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class ShoppingItem(db.Model):
    __tablename__ = "shopping_item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text)
    shopping_list_id = db.Column(
        db.Integer, db.ForeignKey("shopping_list.id"), nullable=False
    )
    quantity = db.Column(db.Float)
    unit = db.Column(db.Text)
    checked = db.Column(db.Boolean, default=False)
