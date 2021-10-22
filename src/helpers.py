from .models import *
from .database import db


# PostDataInterface handles POST request for endpoint /locations/
class PostDataInterface:

    def __init__(self,data):
        if isinstance(data,dict):
            self.data = data
            self.fk = None

    def database_session(self,model):
        db.session.add(model)
        db.session.commit()
        db.session.close()

    def species_model(self):
        data = self.data['species']
        name_of_location = self.data['name']
        location = Locations.query.filter_by(name=name_of_location).first_or_404()
        if isinstance(data,list):
            for d in data:
                if isinstance(d,dict) and 'species_name' in d.keys():
                    self.database_session(Species(d,locations=location))

    def stats_model(self):
        fields = ('stars','rank','unesco_heritage','yearly_visitors')
        if all(self.data['stats'].get(field,0) for field in fields):
            data = self.data['stats']
            name_of_location = self.data['name']
            location = Locations.query.filter_by(name=name_of_location).first_or_404()
            self.database_session(Stats(data,locations=location))
            if self.data.get('species',0):
                self.species_model()

    def geography_model(self):
        fields = ('lat_long','climate','landscape')
        if all(self.data['geography'].get(field,0) for field in fields):
            data = self.data['geography']
            name_of_location = self.data['name']
            location = Locations.query.filter_by(name=name_of_location).first_or_404()
            self.database_session(Geography(data,locations=location))
            if self.data.get('stats',0):
                self.stats_model()

    def locations_model(self):
        self.database_session(Locations(self.data))
        if self.data.get('geography',0):
            self.geography_model()

    def validate(self):
        locations_fields = ('name','country','about')
        if all(self.data.get(field,0) for field in locations_fields):
            self.locations_model()
            return True
        else:
            return False

# request factory for endpoint /locations/
def post_data(data):
    obj = PostDataInterface(data)
    return obj.validate()
