import os
import pytest
from webapp import create_app, db
from webapp.config import basedir


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SECRET_KEY="192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(basedir, "..", "test.db"),
    )

    with app.app_context():
        db.create_all()
