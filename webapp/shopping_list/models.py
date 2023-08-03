from datetime import datetime
from webapp.db import db


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
