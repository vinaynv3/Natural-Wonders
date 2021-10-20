from flask import current_app
from .views import *

"""
Routing System: registers API view class, http methods and endpoints
"""

def register_api(view, endpoint, url):
    view_func = view.as_view(endpoint)
    current_app.add_url_rule(url,view_func=view_func, methods=['GET',])


def app_routes(app):
    with app.app_context():
        register_api(IndexAPI, 'index', '/')
        register_api(LocationsAPI, 'locations', '/locations')
