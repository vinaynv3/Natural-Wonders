from flask.views import MethodView
from .models import *
from .serializer import *


class LandscapeListAPI(MethodView):
    def get(self):
        landscapes_data = Locations.query.all()
        landscapes_schema = LocationsSchema()
        return landscapes_schema.dump(landscapes_data)
