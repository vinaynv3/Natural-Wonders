from flask.views import MethodView
from .models import *
from .serializer import *
from .models import *


class IndexAPI(MethodView):

    def get(self):
        return {'Natural Wonders':'http://api.naturalwonders.com/'}


class LocationsAPI(MethodView):

    def get(self):
        locations = Locations.query.get(1)
        ls = LocationsSchema()
        return ls.dump(locations)
