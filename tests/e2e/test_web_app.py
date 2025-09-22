import pytest
from flask import session

def test_login_required_to_comment(client):
    response = client.post('/comment')
    message = b'You must be logged in to comment'
    assert response.headers['Location'] == 'http://localhost/authentication/login'

def test_new_user_register(client):
    # Check that we can retrieve the registration page.
    status_code = client.get('/authentication/register').status_code
    assert status_code == 200

    # Check that a new user can register.
    user_name = 'new_user'
    password = 'new_password'
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert response.headers['Location'] == 'http://localhost/homepage'

def test_existing_user_register(client):
    # Check that a user cannot register with an existing user name.
    message = b'User name already registered. Please try another.'
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data

    # Check that a user cannot register without a user name.
    user_name = ''
    message = b'User name is required.'
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data

    # Check that a user cannot register without a password.
    user_name = 'new_user2'
    password = ''
    message = b'Password is required.'













    # Note: The second registration attempt in this test function
    # uses the same client session as the first registration attempt.
    # This means that if the first registration was successful then
    # the second attempt will be made when the client is logged in,
    # which is not the situation we want to test. So, we use a new
    # client for the second registration attempt to avoid any error
    # messages about already being logged in overshadowing the error
    # messages we are actually trying to test here about missing`