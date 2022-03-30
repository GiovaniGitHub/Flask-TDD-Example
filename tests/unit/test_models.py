"""
This file (test_models.py) contains the unit tests for the models.py file.
"""
from project.models import User
from faker import Faker 

faker = Faker()
user1 = {'email':faker.email(), 'password':faker.password()}

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password_hashed, authenticated, and active fields are defined correctly
    """
    user = User(user1['email'], user1['password'])
    assert user.email == user1['email']
    assert user.password_hashed !=  user1['password']
    assert user.__repr__() == f"<User: {user1['email']}>"
    assert user.is_authenticated
    assert user.is_active
    assert not user.is_anonymous


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password_hashed fields are defined correctly
    """
    assert new_user.email == user1['email']
    assert new_user.password_hashed != user1['password']


def test_setting_password(new_user):
    """
    GIVEN an existing User
    WHEN the password for the user is set
    THEN check the password is stored correctly and not as plaintext
    """
    new_password = faker.password()
    new_user.set_password(new_password)
    assert new_user.password_hashed != new_password
    assert new_user.is_password_correct(new_password)
    assert not new_user.is_password_correct(user1['password'])


def test_user_id(new_user):
    """
    GIVEN an existing User
    WHEN the ID of the user is defined to a value
    THEN check the user ID returns a string (and not an integer) as needed by Flask-WTF
    """
    new_user.id = 17
    assert isinstance(new_user.get_id(), str)
    assert not isinstance(new_user.get_id(), int)
    assert new_user.get_id() == '17'
