import pytest
from webapp import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_status_index(client):
    assert client.get("/").status_code == 200


def test_status_registration(client):
    assert client.get("/registration").status_code == 200
