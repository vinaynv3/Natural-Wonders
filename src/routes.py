from flask import current_app
from .views import *

"""
Routing System: registers method view API classes
"""

def register_api(view, endpoint, url):
    view_func = view.as_view(endpoint)
    current_app.add_url_rule(url,view_func=view_func, methods=['GET','POST','PUT','DELETE'])

#URL registeration factory with app context
def app_routes(app):
    with app.app_context():
        register_api(IndexAPI, 'index', '/')
        register_api(LocationsAPI, 'locations', '/locations/')
        register_api(LocationAPI, 'location', '/locations/<name>/')

        #error handlers
        @app.errorhandler(404)
        def page_not_found(error):
            msg = {'STATUS':'Not Found',
                    'URL':'http://api.naturalwonders.com/'}
            return msg

        @app.errorhandler(500)
        def internal_server_error(error):
            msg = {'STATUS':'Internal Server Error'}
            return msg

        @app.errorhandler(405)
        def method_not_allowed(error):
            msg = {'STATUS':'Method Not allowed'}
            return msg
