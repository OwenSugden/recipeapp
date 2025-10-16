import os
import pytest
from recipe import create_app
from recipe.adapters.memory_repository import MemoryRepository
from recipe.adapters.populate_repository import populate
from utils import get_project_root
from recipe.adapters.datareader.CSVdatareader import CSVDataReader
from recipe.domainmodel.recipe import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.recipe import RecipeImage
from recipe.domainmodel.recipe import RecipeIngredient
from recipe.domainmodel.recipe import RecipeInstruction
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

TEST_DATA_PATH = get_project_root() / "tests" / "data"


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False,
        'REPOSITORY': 'memory'
    })
    return my_app.test_client()

@pytest.fixture
def auth(client):
    return AuthenticationManager(client)

class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name="Username", password="Password"):
        return self.__client.post(
            "/authentication/login",
            data={"user_name": user_name, "password": password}
        )

    def logout(self):
        return self.__client.get("/authentication/logout")

def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 400

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'foodcooker', 'password': 'Password123!'}
    )

    assert response.headers["Location"] == '/authentication/login'

def test_login(client, auth):
    # Register user first
    client.post('/authentication/register', data={
        'user_name': 'tester', 'password': 'Password123!'
    })
    # Then login
    response = client.post('/authentication/login', data={
        'user_name': 'tester', 'password': 'Password123!'
    })
    assert response.headers['Location'] == '/'

@pytest.mark.parametrize(('user_name', 'password', 'message'), (
    ('', '', b'Your username is required'),
    ('cj', '', b'Your username is too short'),
    ('test', '', b'Your password is required'),
    ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,            a lower case letter and a digit')
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )

    # Assert that the expected byte string message is in the response data
    assert message in response.data

def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session

def test_existing_user_register(client):
    # Seed an existing user
    user_name = 'dup_user'
    password = 'StrongPass1'
    client.post('/authentication/register', data={'user_name': user_name, 'password': password})

    # Try to register again with the same username
    response = client.post('/authentication/register', data={'user_name': user_name, 'password': password})
    assert b'Your username is already taken - please supply another' in response.data

    # Missing username
    response = client.post('/authentication/register', data={'user_name': '', 'password': password})
    assert b'Your username is required' in response.data

    # Missing password
    response = client.post('/authentication/register', data={'user_name': 'new_user2', 'password': ''})
    assert b'Your password is required' in response.data

def test_index_page(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'The Recipe for Connection' in response.data

def test_browse_page(client):
    response = client.get('/browse')
    assert response.status_code == 200
    assert b'Browse Recipes' in response.data

def login_page(client):
    response = client.get('/authentication/login')
    assert response.status_code == 200