from .models import *
from flask import current_app
from slugify import slugify
from .serializer import *
import os
from .helpers import *


#LocationList <endpoint:/locations/>
class LocationList:

    """
    LocationList: cls provides data exchange interface
                  between models and view methods
    GET: returns list of locations
    POST: stores list of location details in models
    (Note: file upload not allowed on endpoint /locations/)
    """

    def __init__(self, data:list=None,
                 placeholder:str=None,picture:str=None):
        self.method = data.method
        self.slug = placeholder
        self.data = data.get_json()

    def get_list(self):
        locations = Locations.query.all()
        schema = LocationsSchema(many=True)
        data = dict(landscape_names=schema.dump(locations),\
                    total=len(locations))
        return data

    #location has one-to-many relationship with other models
    def location_primary_key(self,item):
        location_name = item.get('name',0)
        location = Locations.query.filter_by(name=location_name).first()
        return location

    def species(self,item):
        data = item.get('species',0)
        location = self.location_primary_key(item)
        if isinstance(data,list):
            for d in data:
                if isinstance(d,dict) and 'species_name' in d.keys():
                    database_session(Species(d,locations=location),insert=True)

    def stats(self,item):
        if item.get('stats',0):
            stats_obj = Stats(item.get('stats',0),locations=self.location_primary_key(item))
            database_session(stats_obj,insert=True)
            if item.get('species',0):
                self.species(item)

    # initialize geography details into model Geography
    def geography(self,item):
        _fields = ('climate','landscape')
        if all(item['geography'].get(field,0) for field in _fields):
            geo_obj = Geography(item.get('geography',0),locations=self.location_primary_key(item))
            database_session(geo_obj,insert=True)
            if item.get('stats',0):
                self.stats(item)

    # initialize location details into model Locations
    def location(self,item):
        database_session(Locations(item),insert=True)
        if item.get('geography',0):
            self.geography(item)

    def validate_request_data(self):
        _fields = ('name','country','about')
        if self.data==None or len(self.data) == 0:
            return False
        if isinstance(self.data,dict):
            return False
        for item in self.data:
            x = all(item.get(field,0) for field in _fields)
            y = self.location_primary_key(item)
            z = isinstance(item,dict)
            if x and not y and z:
                self.location(item)
        return True

    def process_request(self):
        _error = {'_response':'only GET and POST \
                                 on endpoint /locations/'}
        _methods = {'GET':self.get_list(),
                    'POST':self.validate_request_data(),}
        if self.method.upper():
            return _methods.get(self.method.upper(),_error)


class LocationName:
    def __init__(self,data,placeholder:str=None,picture:str=None):
        self.data = data.get_json()
        self.slug = placeholder
        self.picture = picture
        self.method = data.method

    def location_name(self):
        location = Locations.query.filter_by(slug=self.slug).first_or_404()
        return location

    def get(self):
        location_schema = LocationSchema()
        return location_schema.dump(self.location_name())

    def update(self):
        locations_fields = ('name','country','about')
        location = self.location_name()
        if any(self.data.get(field,0) for field in locations_fields):
            keys = [field for field in locations_fields if self.data.get(field,0)]
            for key in keys:
                setattr(location,key,self.data[key])
                if key == 'name':
                    setattr(location,'slug',slugify(self.data[key]))
        database_session(location)
        return {'status' :'{0} resource updated'.format(self.slug)}

    def delete(self):
        location = self.location_name()
        filename = location.picture
        folder = current_app.config['UPLOAD_FOLDER']
        for filename.picture in os.listdir(folder):
            file_path = os.path.join(folder, filename.picture)
            os.remove(file_path)
        database_session(location,delete=True)
        return {'status' :'{0} resource deleted'.format(self.slug)}

    def process_request(self):
        if self.method == 'GET':
            return self.get()
        elif self.method == 'PUT':
            return self.update()
        elif self.method == 'DELETE':
            return self.delete()
        return False



class LocationGeo(LocationName):

    def __init__(self,data,placeholder:str=None,picture:str=None):
        super().__init__(data,placeholder,picture)
        self.geography_fields = ('lat_long','climate','landscape')

    def geography_name(self):
        geography = Geography.query.filter_by(locations=self.location_name()).first_or_404()
        return geography

    def validate_data(self):
        if any(self.data.get(field,0) for field in self.geography_fields):
            return True
        return False

    def get(self):
        geography_schema = GeographySchema()
        return geography_schema.dump(self.geography_name())

    def post(self):
        if isinstance(self.data,dict) and self.validate_data():
            location = self.location_name()
            geography = Geography(self.data,locations=location)
            database_session(geography,insert=True)
        return {'status' :'{0} geography details added'.format(self.slug)}

    def update(self):
        geography = self.geography_name()
        if self.validate_data():
            keys = [field for field in self.geography_fields if self.data.get(field,0)]
            for key in keys:
                setattr(geography,key,str(self.data[key]))
        database_session(geography,insert=True)
        return {'status' :'{0} resource geography details updated'.format(self.slug)}

    def delete(self):
        geography = self.geography_name()
        database_session(geography,delete=True)
        return {'status' :'{0} resource geography details deleted'.format(self.slug)}

    def process_request(self):
        if self.method == 'GET':
            return self.get()
        elif self.method == 'POST':
            return self.post()
        elif self.method == 'PUT':
            return self.update()
        elif self.method == 'DELETE':
            return self.delete()
        return False
