import os
from .helpers import *
from flask import current_app,redirect, request,redirect, url_for, send_from_directory
from .datahandler import LocationName
from .serializer import *
from werkzeug.utils import secure_filename
from slugify import slugify

class LocationPic(LocationName):

    """
             **********LocationPicAPI: location image management tool**********
    class is designed to handle only one image per location, http methods below outlines the
    implementation and corresponding location image is found under folder app/media/
    GET: image can be accessed only if image already present in database
    POST: creates new image record in model LocationImage relative to endpoint /locations/<name>/
    PUT: updates image record in model LocationImage relative to endpoint /locations/<name>/
    DELETE: deletes image record in model LocationImage & upload folder relative to endpoint /locations/<name>/
    """
    def __init__(self,data,placeholder:str=None,picture:str=None,specie:str=None):
        super().__init__(data,placeholder,picture,specie)
        self.files = data.files


    def pic_name(self):
        pic = LocationImage.query.filter_by(locations=self.location_name()).first()
        return pic

    def get(self):
        pic_schema = LocationImageSchema()
        pic = self.pic_name()
        if pic:
            return pic_schema.dump(pic)
        return {}

    def post(self):
        model = LocationImage
        location = self.location_name()
        save_file(self.files,model,location,self.slug)
        return redirect(url_for('location_picture', name=self.slug,_method='GET'))

    def put(self):
        f = list(self.files.keys())[0]
        if not validate_file(self.files,f):
            return {'status':'missing file in content type header for record {0}'.format(self.name)}
        if self.pic_name():
            delete_file(self.pic_name())
            self.post()
            return self.get()


    def process_request(self):
        if self.method == 'GET':
            return self.get()
        elif self.method == 'POST':
            return self.post()
        elif self.method == 'PUT':
            return self.put()

        return False

#---------------------------------------------------------------------------------------#

class LocationDwnldPic(LocationName):

    def __init__(self,data,placeholder:str=None,picture:str=None,specie:str=None):
        super().__init__(data,placeholder,picture,specie)
        self.filename = picture

    def pic_name(self):
        pic = LocationImage.query.filter_by(locations=self.location_name()).first()
        return pic

    def get(self):
        folder = current_app.config['UPLOAD_FOLDER']
        if self.filename in os.listdir(folder):
            return send_from_directory(folder, self.filename)
        return {}

    def delete(self):
        if self.location_name().picture:
            filename = self.pic_name()
            if delete_file(filename):
                return {'status':'{0} deleted for record {1}'.format(filename.picture,self.slug),
                        '_link':url_for('location_picture',name=self.slug,_method='GET')}

    def process_request(self):
        if self.method == 'GET':
            return self.get()
        elif self.method == 'DELETE':
            return self.delete()
        return False

#----------------------------------------------------------------------------------#

class LocationSpecies(LocationName):

    def __init__(self,data,placeholder:str=None,picture:str=None,specie:str=None):
        super().__init__(data,placeholder,picture,specie)
        self.species_fields = ['species_name']

    def species_all(self):
        species = Species.query.filter_by(locations=self.location_name()).all()
        return species

    def validate_data(self,item):
        if all(item.get(field,0) for field in self.species_fields):
            return True
        return False

    def validate_specie(self,specie):
        species = self.species_all()
        if specie in [specie.species_name for specie in species]:
            return True
        return False

    def get(self):
        species_schema = SpeciesSchema()
        species = species_schema.dump(self.species_all(),many=True)
        return dict(species=species,total=len(species))

    def post(self):
        for item in self.data:
            specie = item.get('species_name',' ')
            x = isinstance(item,dict)
            y =  self.validate_data(item)
            z = self.validate_specie(specie)
            print(x,y,z)
            if x and y and not z:
                location = self.location_name()
                species = Species(item,locations=location)
                database_session(species,insert=True)
        return redirect(url_for('location_species', name=self.slug,_method='GET'))

    def delete(self):
        species = self.species_all()
        if len(species) > 0:
            for specie in species:
                database_session(specie,delete=True)
        return redirect(url_for('location_species', name=self.slug,_method='GET'))

    def process_request(self):
        if self.method == 'GET':
            return self.get()
        elif self.method == 'POST':
            return self.post()
        elif self.method == 'DELETE':
            return self.delete()
        return False

#----------------------------------------------------------------------------------#

class LocationSpecie(LocationName):
    def __init__(self,data,placeholder:str=None,picture:str=None,specie:str=None):
        super().__init__(data,placeholder,picture,specie)
        self.files = data.files
        self.sp_slug = specie
        self.specie_fields = ('species_name','endangered','pic','sp_class')

    def specie_name(self):
        specie = Species.query.filter_by(locations=self.location_name(),sp_slug=self.sp_slug).first()
        return specie

    def get(self):
        sp_schema = SpeciesSchema()
        specie_serializer = sp_schema.dump(self.specie_name())
        if self.specie_name().pic:
            return specie_serializer
        return specie_serializer

    def file_handler(self):

        specie = self.specie_name()
        f = list(self.files.keys())[0]
        url = url_for('location_specie', name=self.slug,
                                    specie_name=self.sp_slug,_method='GET')
        if not validate_file(self.files,f):
            return {'status':'missing file in content type header for record {0}'.format(self.name),
                    'url':url}

        file = self.files.get(f,0)
        filename = secure_filename(file.filename)
        setattr(specie,'pic',filename)
        database_session(specie,insert=True)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return True

    def validate_keys(self):
        keys = [field for field in self.specie_fields if self.data.get(field,0) \
                                                            and field != 'pic']
        if 'endangered' not in keys and 'endangered' in self.data.keys():
            keys.append('endangered')
        return keys

    def json_handler(self):
        specie = self.specie_name()
        keys = self.validate_keys()
        for key in keys:
            if key == 'species_name':
                setattr(specie,'sp_slug',slugify(self.data[key]))
            setattr(specie,key,self.data[key])
        database_session(specie,insert=True)
        return True

    def remove_file(self):
        specie = self.specie_name()
        folder = current_app.config['UPLOAD_FOLDER']
        if specie.pic in os.listdir(folder):
            file_path = os.path.join(folder,specie.pic)
            os.remove(file_path)
        return True

    def put(self):
        specie = self.specie_name()
        if self.data:
            self.json_handler()
            keys = self.validate_keys()
            url = url_for('location_specie',name=self.slug,specie_name=self.sp_slug,_method='GET')
            if 'species_name' in keys:
                s = Species.query.filter_by(species_name=self.data['species_name']).first()
                url = url_for('location_specie',name=self.slug,specie_name=s.sp_slug,_method='GET')
                return dict(status="Resource updated",url=url)
            return dict(status="Resource updated",url=url)

        elif not specie.pic:
            self.file_handler()
            return self.get()
        elif self.data and self.files:
            self.json_handler()
            self.remove_file()
            self.file_handler()
            return dict(status="Resource updated")
        elif specie.pic:
            self.remove_file()
            self.file_handler()
            return self.get()
        else:
            return dict(status="invalid data, please verify")

    def delete(self):
        specie = self.specie_name()
        if specie:
            self.remove_file()
            database_session(specie,delete=True)
            return {'status':'({0}) > {1} specie record removed'.format(self.slug,self.sp_slug),
                    'url':url_for('location_species', name=self.slug,_method='GET')}

    def process_request(self):
        if self.method == 'GET':
            return self.get()
        elif self.method == 'PUT':
            return self.put()
        elif self.method == 'DELETE':
            return self.delete()
        return False

#---------------------------------------------------------------------------------------#

class LocationSpeciePicDwnld(LocationName):

    def __init__(self,data,placeholder:str=None,picture:str=None,specie:str=None):
        super().__init__(data,placeholder,picture,specie)
        self.filename = picture
        self.specie = specie


    def get(self):
        folder = current_app.config['UPLOAD_FOLDER']
        if self.filename in os.listdir(folder):
            return send_from_directory(folder, self.filename)
        return {}

    def delete(self):
        specie = Species.query.filter_by(pic=self.filename).first()
        folder = current_app.config['UPLOAD_FOLDER']
        url = url_for('location_specie',name=self.slug,specie_name=self.specie,_method='GET')
        if specie and self.filename in os.listdir(folder):
            setattr(specie,'pic',None)
            database_session(specie,insert=True)
            file_path = os.path.join(folder,self.filename)
            os.remove(file_path)
            return {'status':'{0} deleted for record {1}'.format(self.filename,self.specie),
                    'url':url}

    def process_request(self):
        if self.method == 'GET':
            return self.get()
        if self.method == 'DELETE':
            return self.delete()
        return False
