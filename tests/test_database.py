import os
import tempfile

import pytest
from src import create_app
from src.database import init_db
from src.models import *
from src.serializer import *

@pytest.fixture
def client():
    db_fd,db_path = tempfile.mkstemp()

    app = create_app({'TESTING': True, 'DATABASE': db_path})
    with app.test_client() as client:
        with app.app_context():
            init_db(app)
        yield client

    os.close(db_fd)
    os.unlink(db_path)

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No' in rv.data

def test_models(client):

    user = Locations(name = "Niagara Falls",country="canada"\
                        ,about = "Its a beautiful water falls")
    user_schema = LocationsSchema()
    assert {} != user_schema.dump(user)
