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
    ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,            a lower case letter and a digit')
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

def test_login_required_to_comment(client, memory_repo):
    # pick a real recipe id
    recipe_id = memory_repo.get_all_recipes()[0].id

    # not logged in → should redirect to login
    response = client.post(f'/browse/{recipe_id}/comment', data={'comment': 'hi'}, follow_redirects=False)
    assert response.status_code in (302, 303)
    assert response.headers['Location'] == '/authentication/login'


def test_redirect_to_login_after_comment(client, memory_repo):
    recipe_id = memory_repo.get_all_recipes()[0].id
    resp = client.post(f'/browse/{recipe_id}/comment',
                       data={'comment': 'hi'},
                       follow_redirects=False)
    assert resp.status_code in (302, 303)
    assert resp.headers['Location'] == '/authentication/login'


def test_redirect_to_login_after_rating(client, memory_repo):
    recipe_id = memory_repo.get_all_recipes()[0].id
    resp = client.post(f'/rate/{recipe_id}',
                       data={'rating': '5'},
                       follow_redirects=False)
    assert resp.status_code in (302, 303)
    assert resp.headers['Location'] == '/authentication/login'


def test_new_user_register(client):
    # GET register page
    assert client.get('/authentication/register').status_code == 200

    # POST valid registration → redirect to login
    response = client.post(
        '/authentication/register',
        data={'user_name': 'new_user', 'password': 'New_Password1'},
        follow_redirects=False
    )
    assert response.status_code in (302, 303)
    assert response.headers['Location'] == '/authentication/login'

def test_existing_user_register(client):
    # Seed an existing user
    user_name = 'dup_user'
    password = 'StrongPass1'
    client.post('/authentication/register', data={'user_name': user_name, 'password': password})

    # Try to register again with the same username
    response = client.post('/authentication/register', data={'user_name': user_name, 'password': password})
    assert b'Your user_profile name is already taken - please supply another' in response.data

    # Missing username
    response = client.post('/authentication/register', data={'user_name': '', 'password': password})
    assert b'Your user_profile name is required' in response.data

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

def test_recipe_details_page(client, memory_repo):
    # grab the first available recipe from the repo
    recipe = memory_repo.get_all_recipes()[0]
    recipe_id = recipe.id

    response = client.get(f'/browse/{recipe_id}')
    assert response.status_code == 200

def login_page(client):
    response = client.get('/authentication/login')
    assert response.status_code == 200