from flask import current_app
from .views import *

"""
Routing System: registers method view API classes
"""

def register_api(view, endpoint, url,methods):
    view_func = view.as_view(endpoint)
    current_app.add_url_rule(url,view_func=view_func, methods=methods)

#URL registeration factory with app context
def app_routes(app):
    with app.app_context():
        register_api(IndexAPI, 'index', '/',['GET'])
        register_api(LocationsAPI, 'locations', '/locations/',['GET','POST'])
        register_api(LocationAPI, 'location', '/locations/<name>/',['GET','POST','PUT','DELETE'])
        register_api(LocationImageAPI, 'location_picture', '/locations/image/<name>/',['GET','POST','PUT','DELETE'])

        #error handlers
        @app.errorhandler(404)
        def page_not_found(error):
            msg = {'Error_Msg':str(error)}
            return msg

        @app.errorhandler(500)
        def internal_server_error(error):
            msg = {'Error_Msg':str(error)}
            return msg

        @app.errorhandler(405)
        def method_not_allowed(error):
            msg = {'Error_Msg':str(error)}
            return msg

        @app.errorhandler(413)
        def request_file_is_too_large(error):
            msg = {'Error_Msg':str(error)}
            return msg
