
DEBUG = True

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:////" + os.path.join(BASE_DIR, "db.sqlite3")
SQLALCHEMY_TRACK_MODIFICATIONS=False
UPLOAD_FOLDER = os.path.join(BASE_DIR.split('instance')[0],'media')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1000 * 1000
JSON_SORT_KEYS=False
