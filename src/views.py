from flask.views import MethodView
from .models import *
from .serializer import *
from .models import *


class IndexAPI(MethodView):

    def get(self):
        return {'Natural Wonders':'http://api.naturalwonders.com/'}


class LocationsAPI(MethodView):

    def get(self):
        locations = Locations.query.all()
        locations_schema = LocationsSchema(many=True)
        data = dict(natural_wonders=locations_schema.dump(locations),
                    total=len(locations))
        return data

    def post(self,**kwargs):
        pass
