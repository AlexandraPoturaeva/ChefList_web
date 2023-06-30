from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    shopping_lists = db.relationship("ShoppingList", backref="user", lazy=True)

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


class ProductCategorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    color = db.Column(db.Text)

    def __repr__(self):
        return f"<ProductCategory: {self.name}, color: {self.color}>"


class RecipeCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    color = db.Column(db.Text)

    def __repr__(self):
        return f"<RecipeCategory: {self.name}, color: {self.color}>"


class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True, index=True)

    def __repr__(self):
        return f"<Unit: {self.name}>"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, index=True, unique=True)
    category_id = db.Column(
        db.Integer, db.ForeignKey(ProductCategorie.id), nullable=False
    )

    def __repr__(self):
        return f"<Product: {self.name}, category: {self.category_id}>"


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("recipe_category.id"))
    description = db.Column(db.Text)
    preparation_time = db.Column(db.Text)
    cooking_time = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Recipe: {self.name} by user with id {self.user_id}>"


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Float, nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey("unit.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))

    def __str__(self):
        product_name = db.session.query(Product).get(self.product_id).name
        unit_name = db.session.query(Unit).get(self.unit_id).name
        return f"{product_name}, {self.quantity} {unit_name}"

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
    shopping_list_id = db.Column(
        db.Integer, db.ForeignKey("shopping_list.id"), nullable=False
    )
    quantity = db.Column(db.Float)
    selected = db.Column(db.Boolean, default=False)
