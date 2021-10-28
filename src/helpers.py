from .models import *
from .database import db
from slugify import slugify


# database session handler
def database_session(model,delete=False):

    db.session.add(model)
    db.session.commit()
    db.session.close()
    if delete:
        db.session.delete(model)
        db.session.commit()
        db.session.close()


# PostDataInterface handles POST request for endpoint /locations/
class PostLocationsData:

    def __init__(self,data,placeholder=None):
        if isinstance(data,dict):
            self.data = data

    def species_model(self):
        data = self.data['species']
        name_of_location = self.data['name']
        location = Locations.query.filter_by(name=name_of_location).first_or_404()
        if isinstance(data,list):
            for d in data:
                if isinstance(d,dict) and 'species_name' in d.keys():
                    database_session(Species(d,locations=location))

    def stats_model(self):
        fields = ('stars','unesco_heritage','yearly_visitors')
        if all(self.data['stats'].get(field,0) for field in fields):
            data = self.data['stats']
            name_of_location = self.data['name']
            location = Locations.query.filter_by(name=name_of_location).first_or_404()
            database_session(Stats(data,locations=location))
            if self.data.get('species',0):
                self.species_model()

    def geography_model(self):
        fields = ('lat_long','climate','landscape')
        if all(self.data['geography'].get(field,0) for field in fields):
            data = self.data['geography']
            name_of_location = self.data['name']
            location = Locations.query.filter_by(name=name_of_location).first_or_404()
            database_session(Geography(data,locations=location))
            if self.data.get('stats',0):
                self.stats_model()

    def locations_model(self):
        database_session(Locations(self.data))
        if self.data.get('geography',0):
            self.geography_model()

    def validate(self):
        locations_fields = ('name','country','about')
        if all(self.data.get(field,0) for field in locations_fields):
            self.locations_model()
            return {'status' :' new resource created'}
        else:
            return {'status':'fields or data you entered are incorrect'}



class PutLocationData:
    def __init__(self,data,slug):
        if isinstance(data,dict):
            self.data = data
            self.name_slug = slug

    def location_model_update(self,keys):
        location = Locations.query.filter_by(slug=self.name_slug).first_or_404()
        for key in keys:
            setattr(location,key,self.data[key])
            if key == 'name':
                setattr(location,'slug',slugify(self.data[key]))
        database_session(location)

    def validate(self):
        locations_fields = ('name','country','about')
        if any(self.data.get(field,0) for field in locations_fields):
            self.location_model_update([field for field in locations_fields if self.data.get(field,0)])
            return {'status' :'resource updated'}
        else:
            return {'status' :'something went wrong, please re-verify data'}

class DeleteLocationData(PutLocationData):

    def __init__(self,data,slug):
        super().__init__(data,slug)

    def location_model_delete(self):
        location = Locations.query.filter_by(slug=self.name_slug).first_or_404()
        database_session(location,delete=True)
        return {'status' :'resource deleted'}


# request data management factory for endpoints for url /locations/ and after
def request_data_handler(data,view_cls_name,placeholder=None,delete=False):

    data_handlers = {'LocationsAPI':PostLocationsData,
                    'LocationAPI':PutLocationData,}
    if delete:
        return DeleteLocationData(data,placeholder).location_model_delete()
    else:
        object = data_handlers.get(view_cls_name,None)(data,placeholder)
        print(view_cls_name,object)
        return object.validate()
