from datetime import datetime
from webapp.db import db, ma

PRODUCT_CATEGORIES = {
    0: ["Хлебобулочные изделия", "Bakery/Bread"],
    1: ["Здоровое питание", "Health Foods"],
    2: ["Специи и приправы", "Spices and Seasonings"],
    3: ["Всё для выпечки", "Baking"],
    4: ["Макаронные изделия, крупы", "Pasta and Rice"],
    5: ["Охлаждённые продукты", "Refrigerated"],
    6: ["Консервированные продукты", "Canned and Jarred"],
    7: ["Замороженные продукты", "Frozen"],
    8: ["Варенье, мёд, ореховая паста", "Nut butters, Jams, and Honey"],
    9: ["Масло, уксус, заправка для салата", "Oil, Vinegar, Salad Dressing"],
    10: ["Соусы", "Condiments"],
    11: ["Закуски, снэки"],
    12: ["Молоко, молочные продукты, яйца", "Milk, Eggs, Other Dairy"],
    13: ["Этнические продукты", "Ethnic Foods"],
    14: ["Чай, кофе", "Tea and Coffee"],
    15: ["Мясо, птица", "Meat"],
    16: ["Деликатесы", "Gourmet"],
    17: ["Сладости", "Sweet Snacks"],
    18: ["Без глютена", "Gluten Free"],
    19: ["Алкогольные напитки", "Alcoholic Beverages"],
    20: ["Быстрые завтраки", "Cereal"],
    21: ["Орехи", "Nuts"],
    22: ["Напитки", "Beverages"],
    23: ["Овощи и фрукты", "Produce"],
    24: ["Домашнее производство", "Not in Grocery Store/Homemade"],
    25: ["Морепродукты", "Seafood"],
    26: ["Сыр", "Cheese"],
    27: ["Сухофрукты", "Dried Fruits"],
    28: ["Онлайн", "Online"],
    29: ["Товары для гриля", "Grilling Supplies"],
    30: ["Хлеб", "Bread"],
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
    name_ru = db.Column(db.Text, nullable=False, index=True, unique=True)
    name_en = db.Column(db.Text, nullable=False, index=True)
    category = db.Column(db.Integer)

    def __repr__(self):
        return f"<Product: {self.name}, category: {self.category}>"


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category = db.Column(db.Integer)
    servings = db.Column(db.Integer, nullable=False)
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


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product


class RecipeDescriptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RecipeDescription
        exclude = ("id",)


class IngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ingredient
        exclude = ("id",)

    product = ma.Nested(nested=ProductSchema)


class RecipeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe

    ingredients = ma.Nested(nested=IngredientSchema, many=True)
    description = ma.Nested(nested=RecipeDescriptionSchema, many=True)
