from flask import current_app
from .views import *

"""
Routing System: registers method view api's
"""

# urls registry
def register_api(view, endpoint, url,methods):
    view_func = view.as_view(endpoint)
    current_app.add_url_rule(url,view_func=view_func, methods=methods)


#URL registeration factory and error handlers with app context
def app_routes(app):
    with app.app_context():

        register_api(IndexAPI, 'index', '/',['GET'])
        register_api(LocationsAPI, 'locations', '/locations/',['GET','POST'])
        register_api(LocationAPI, 'location', '/locations/<name>',\
                                  ['GET','PUT','DELETE'])
        register_api(LocationGeoAPI, 'location_geography', '/locations/<name>/geo',\
                                  ['GET','POST','PUT','DELETE'])
        register_api(LocationStatsAPI, 'location_stats', '/locations/<name>/stats',\
                                  ['GET','POST','PUT','DELETE'])
        register_api(LocationPicAPI, 'location_picture', '/locations/<name>/pic',\
                                    ['GET','POST','PUT'])
        register_api(PicDownloadAPI, 'dwnld_pic', '/locations/<name>/pic/<filename>',['GET','DELETE'])
        register_api(LocationSpeciesAPI, 'location_species', '/locations/<name>/species',\
                                         ['GET','POST','DELETE'])
        register_api(LocationSpecieAPI, 'location_specie', \
                         '/locations/<name>/species/<specie_name>',['GET','PUT','DELETE'])
        register_api(SpeciePicDwnldAPI, 'specie_dwnld_pic', \
                                        '/locations/<name>/species/<specie_name>/<file>',['GET','DELETE'])


        #error handlers
        @app.errorhandler(404)
        def page_not_found(error):
            msg = {'Error_Code':error.code,
                    'Error_Msg':str(error)}
            return msg

        @app.errorhandler(500)
        def internal_server_error(error):
            msg = {'Error_Code':error.code,
                    'Error_Msg':str(error)}
            return msg

        @app.errorhandler(405)
        def method_not_allowed(error):
            msg = {'Error_Code':error.code,
                    'Error_Msg':str(error)}
            return msg

        @app.errorhandler(413)
        def request_file_is_too_large(error):
            msg = {'Error_Code':error.code,
                    'Error_Msg':str(error)}
            return msg

        @app.errorhandler(400)
        def bad_request(error):
            msg = {'Error_Code':error.code,
                    'Error_Msg':str(error)}
            return msg
