import pytest
from project import create_app, db
from project.models import User
from faker import Faker


faker = Faker()

user1 = {'email':faker.email(), 'password_plaintext':faker.password()}

@pytest.fixture(scope='module')
def new_user():
    user = User(user1['email'], user1['password'])
    return user


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(user1['email'], user1['password'])
    user2 = User(faker.email(), faker.password())
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()


@pytest.fixture(scope='function')
def login_default_user(test_client):
    test_client.post('/login', data=dict(email=user1['email'], password=user1['password']),
                     follow_redirects=True)

    yield  # this is where the testing happens!

    test_client.get('/logout', follow_redirects=True)
