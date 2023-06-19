from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    shopping_lists = db.relationship('ShoppingList', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User {self.id} ' \
               f'\nemail: {self.email} ' \
               f'\nname: {self.name}' \
               f'\ncreated_at {self.created_at}'


class ShoppingList(db.Model):
    __tablename__ = 'shopping_list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shopping_items = db.relationship('ShoppingItem', backref='shopping_list', lazy=True)
    public_id = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class ShoppingItem(db.Model):
    __tablename__ = 'shopping_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    shopping_list_id = db.Column(db.Integer, db.ForeignKey('shopping_list.id'), nullable=False)
    quantity = db.Column(db.Float)
    selected = db.Column(db.Boolean, default=False)


