from flask.views import MethodView
from .models import *
from .serializer import *
from flask import request
from .helpers import post_data



class IndexAPI(MethodView):

    def get(self):
        return {'Natural Wonders':'http://api.naturalwonders.com/',
                'locations':'http://api.naturalwonders.com/locations/',
                }


class LocationsAPI(MethodView):

    def get(self):
        locations = Locations.query.all()
        locations_schema = LocationsSchema(many=True)
        data = dict(natural_wonders=locations_schema.dump(locations),
                    total=len(locations))
        return data

    def post(self,*args,**kwargs):
        if post_data(request.get_json()):
            return {'status' :'new resource has been created'}
        else:
            return {'status':'fields or data you entered is incorrect'}
