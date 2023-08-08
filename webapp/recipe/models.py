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
    0: ["Супы", "soup"],
    1: ["Основные блюда", "main course"],
    2: ["Гарниры", "side dish"],
    3: ["Завтраки", "breakfast"],
    4: ["Закуски", "fingerfood"],
    5: ["Снэки", "snack"],
    6: ["Аппетайзеры", "appetizer"],
    7: ["Салаты", "salad"],
    8: ["Соусы", "sauce"],
    9: ["Напитки", "beverage"],
    10: ["Алкогольные напитки", "drink"],
    11: ["Десерты", "dessert"],
    12: ["Выпечка", "bread"],
    13: ["Маринады", "marinade"],
}

CUISINES = {
    0: ["Африканская", "African"],
    1: ["Азиатская", "Asian"],
    2: ["Американская", "American"],
    3: [
        "Британская",
        "British",
    ],
    4: [
        "Каджунская",
        "Cajun",
    ],
    5: [
        "Карибская",
        "Caribbean",
    ],
    6: [
        "Китайская",
        "Chinese",
    ],
    7: [
        "Восточноевропейская",
        "Eastern European",
    ],
    8: [
        "Европейская",
        "European",
    ],
    9: [
        "Французская",
        "French",
    ],
    10: [
        "Немецкая",
        "German",
    ],
    11: [
        "Греческая",
        "Greek",
    ],
    12: [
        "Индийская",
        "Indian",
    ],
    13: [
        "Ирландская",
        "Irish",
    ],
    14: [
        "Итальянская",
        "Italian",
    ],
    15: [
        "Японская",
        "Japanese",
    ],
    16: [
        "Еврейская",
        "Jewish",
    ],
    17: [
        "Корейская",
        "Korean",
    ],
    18: [
        "Латиноамериканская",
        "Latin American",
    ],
    19: [
        "Средиземноморская",
        "Mediterranean",
    ],
    20: [
        "Мексиканская",
        "Mexican",
    ],
    21: [
        "Ближневосточная",
        "Middle Eastern",
    ],
    22: [
        "Северная",
        "Nordic",
    ],
    23: [
        "Южная",
        "Southern",
    ],
    24: [
        "Испанская",
        "Spanish",
    ],
    25: [
        "Тайская",
        "Thai",
    ],
    26: [
        "Вьетнамская",
        "Vietnamese",
    ],
}

DIETS = {
    0: ["Безглютеновая", "Gluten Free"],
    1: ["Кетогенная", "Ketogenic"],
    2: ["Вегетарианская", "Vegetarian"],
    3: ["Лакто-вегетаринская", "Lacto-Vegetarian"],
    4: ["Ово-вегетаринская", "Ovo-Vegetarian"],
    5: ["Веганская", "Vegan"],
    6: ["Пескетарианская", "Pescetarian"],
    7: ["Палео", "Paleo"],
    8: ["Праймал", "Primal"],
    9: ["Low FODMAP", "Low FODMAP"],
    10: ["Whole30", "Whole30"],
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
    cuisine = db.Column(db.Integer)
    diet = db.Column(db.Integer)
    description = db.relationship(
        "RecipeDescription", backref="recipe", lazy=True, cascade="all, delete"
    )
    cooking_time = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ingredients = db.relationship(
        "Ingredient", backref="recipe", lazy=True, cascade="all, delete"
    )

    def __repr__(self):
        return f"<Recipe: {self.name} by user with id {self.user_id}>"


class RecipeDescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))


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
