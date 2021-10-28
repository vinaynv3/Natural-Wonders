from flask.views import MethodView
from .models import *
from .serializer import *
from flask import request
from .helpers import request_data_handler



class IndexAPI(MethodView):

    def get(self):
        return {'Natural Wonders':'http://api.naturalwonders.com/',
                'locations':'http://api.naturalwonders.com/locations/',
                'location':'http://api.naturalwonders.com/locations/<name>/',
                }


class LocationsAPI(MethodView):

    __name = 'LocationsAPI'
    def get(self):
        locations = Locations.query.all()
        locations_schema = LocationsSchema(many=True)
        data = dict(natural_wonders=locations_schema.dump(locations),
                    total=len(locations))
        return data

    def post(self,*args,**kwargs):
        return request_data_handler(request.get_json(),self.__name)


class LocationAPI(MethodView):

    __name = 'LocationAPI'

    def get(self,name):
        location = Locations.query.filter_by(slug=name).first_or_404()
        location_schema = LocationSchema()
        data = location_schema.dump(location)
        return data

    def post(self,name):
        return {'status' :'requested http method not allowed for corresponding endpoint'}

    def put(self, name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request.get_json(),self.__name,placeholder=name)

    def delete(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request.get_json(),self.__name,placeholder=name,delete=True)

class ImageUploadAPI(MethodView):

    def get(self):
        pass

    def post(self,*args,**kwargs):
        pass
