from webapp.model import db, User
from webapp import create_app
from datetime import datetime


def test_add_user(app, db, Model):
    user = Model(
        email='example@example.com',
        password_hash='123',
        name='Иван Иванов',
        created_at=datetime.now()
    )

    with app.app_context():
        db.session.add(user)
        db.session.commit()
        data = Model.query.filter_by(email='example@example.com').first()
        db.session.delete(data)
        db.session.commit()

    assert data == user
    return data


if __name__ == '__main__':
    print(test_add_user(create_app(), db, User))

