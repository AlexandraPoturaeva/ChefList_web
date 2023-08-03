import pytest
from webapp import create_app
from webapp.db import db
from webapp.db import User


@pytest.fixture()
def app():
    app = create_app(database_uri="sqlite://", secret_key="test_secret_key")
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.mark.parametrize("url", ["/", "/registration"])
def test_public_pages_status_code(client, url):
    assert client.get(url).status_code == 200


def test_registration(client, app):
    client.post(
        "/process-reg",
        data={
            "name": "test",
            "email": "test@example.com",
            "password": "testpassword",
            "password2": "testpassword",
        },
    )

    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "test@example.com"

    client.post(
        "/login",
        data={"email": "test@example.com", "password": "testpassword"},
        follow_redirects=True,
    )

    assert client.get("/profile").status_code == 200
