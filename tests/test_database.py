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
    app = create_app({'TESTING': True, 'DATABASE': db_path,
                    'SQLALCHEMY_TRACK_MODIFICATIONS':False})
    with app.test_client() as client:
        with app.app_context():
            init_db(app)
        yield client

    os.close(db_fd)
    os.unlink(db_path)

def test_empty_db(client):
    """Start with a blank database."""

    get = client.get('/')
    assert b'natural_wonders_api_docs' in get.data

def test_models(client):
    print(dir(client))
    data = dict(name = "Algonquin park",country="on,canada"\
                        ,about = "Its a beautiful water park")

    location = Locations(data)
    locations_schema = LocationsSchema()
    assert {} != locations_schema.dump(location)
