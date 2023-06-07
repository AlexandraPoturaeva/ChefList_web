from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'User {self.id} ' \
               f'\nemail: {self.email} ' \
               f'\npassword_hash: {self.password_hash} ' \
               f'\nname: {self.name}' \
               f'\ncreated_at {self.created_at}'
