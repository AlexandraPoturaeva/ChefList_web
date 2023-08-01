from datetime import datetime
from webapp.db import db

PRODUCT_CATEGORIES = {
    "Хлебобулочные изделия": "burlywood",
    "Кондитерские изделия": "goldenrod",
    "Молоко, сыр, яйца": "seashell",
    "Мясо, птица": "brown",
    "Сосиски, колбасы, деликатесы": "salmon",
    "Рыба и морепродукты": "steelblue",
    "Овощи и фрукты": "limegreen",
    "Бакалея, соусы": "hotpink",
    "Напитки": "magenta",
    "Чай, кофе, какао": "rosybrown",
    "Чипсы, орехи, сухарики": "tomato",
    "Замороженные продукты": "lightskyblue",
    "Консервы, мёд, варенье": "gray",
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
