import pytest
from backend.app import app as flask_app
from backend.db import db
from backend.auth import login as auth_login

@pytest.fixture
def app():
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def token():
    return auth_login("admin", "password")
