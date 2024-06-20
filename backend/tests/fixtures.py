import pytest
from flask_jwt_extended import create_access_token

from ..src.app import create_app

# Fixture for creating the app
@pytest.fixture()
def app():
    yield create_app()

# Fixture for creating a test client
@pytest.fixture()
def client(app):
    yield app.test_client()
    
# Fixture for creating an access token - simulating a logged in user
@pytest.fixture()
def auth_headers(app):
    with app.app_context():
        access_token = create_access_token(identity="asd@asd")
        return {"Authorization": f"Bearer {access_token}"}
    