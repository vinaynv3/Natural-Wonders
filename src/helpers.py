from .database import db
from flask import current_app


# database session handler
def database_session(model,insert=False,delete=False):
    try:
        storage = db.session
        if insert:
            storage.add(model)
        elif delete:
            storage.delete(model)
        else:
            return
    finally:
        storage.commit()
        storage.close()
