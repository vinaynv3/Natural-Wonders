
import os
from flask import Flask

#application_factory:flask app and its configurations
def create_app(test_config=None):

    """
    function creates flask app instance,loads configurations
    details from instance path from file config.py
    """
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #app contexts
    from . import database
    database.init_db(app)
    from . import serializer
    serializer.init_marshmallow(app)
    from . import routes
    routes.app_routes(app)

    return app
