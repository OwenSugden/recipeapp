import pytest
from flask import session

def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'foodcooker', 'password': 'IloveCooking982'}
    )
    assert response.headers['Location'] == '/authentication/login'

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
    ('', '', b'Your user_profile name is required'),
    ('cj', '', b'Your user_profile name is too short'),
    ('test', '', b'Your password is required'),
    ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,            a lower case letter and a digit'),
    ('fmercury', 'Test#6^0', b'Your user_profile name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session

def test_login_required_to_comment(client):
    response = client.post('/comment')
    message = b'You must be logged in to comment'
    assert response.headers['Location'] == 'http://localhost/authentication/login'

def test_new_user_register(client):
    # Check that we can retrieve the registration page.
    status_code = client.get('/authentication/register').status_code
    assert status_code == 200

    # Check that a new user_profile can register.
    user_name = 'new_user'
    password = 'new_password'
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert response.headers['Location'] == 'http://localhost/homepage'

def test_existing_user_register(client, user_name=None, password=None):
    # Check that a user_profile cannot register with an existing user_profile name.
    message = b'User name already registered. Please try another.'
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data

    # Check that a user_profile cannot register without a user_profile name.
    user_name = ''
    message = b'User name is required.'
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data

    # Check that a user_profile cannot register without a password.
    user_name = 'new_user2'
    password = ''
    message = b'Password is required.'

def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'The Recipe for Connection' in response.data

def test_browse(client):
    response = client.get('/browse')
    assert response.status_code == 200
    assert b'Browse Recipes' in response.data

def test_recipe_details(client, memory_repo):
    # grab the first available recipe from the repo
    recipe = memory_repo.get_all_recipes()[0]
    recipe_id = recipe.id

    response = client.get(f'/browse/{recipe_id}')
    assert response.status_code == 200













    # Note: The second registration attempt in this test function
    # uses the same client session as the first registration attempt.
    # This means that if the first registration was successful then
    # the second attempt will be made when the client is logged in,
    # which is not the situation we want to test. So, we use a new
    # client for the second registration attempt to avoid any error
    # messages about already being logged in overshadowing the error
    # messages we are actually trying to test here about missing`