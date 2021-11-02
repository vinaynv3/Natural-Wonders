
import os
import json
from slugify import slugify
from flask.views import MethodView
from flask import request, current_app,redirect, url_for
from .models import *
from .interface import request_data_handler



#view<endpoint:/>
class IndexAPI(MethodView):

    def get(self):
        path = os.path.abspath(os.path.dirname(__file__))
        os.chdir(path)
        with open("index.json","r") as file:
            data = json.load(file)
            return data


#view<endpoint:/locations>
class LocationsAPI(MethodView):

    __name = 'LocationsAPI'
    def get(self):
        return request_data_handler(request,self.__name)

    def post(self):
        status = request_data_handler(request,self.__name)
        if status:
            return redirect(url_for('locations',_method='GET'))
        else:
            return {'status':'incorrect data format, post location dict object or objects in a list'}


#view<endpoint:/locations/<name>>
class LocationAPI(MethodView):

    __name = 'LocationAPI'
    def get(self,name):
        return request_data_handler(request,self.__name,placeholder=name)

    def put(self, name):
        l = Locations.query.filter_by(slug=name).first_or_404()
        if l and request.get_json():
            return request_data_handler(request,self.__name,placeholder=name)
        return {"status":"{0} request payload seems empty, please verify".format(name)}

    def delete(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)


#view<endpoint:/location/<name>/geo>
class LocationGeoAPI(MethodView):

    __name = 'LocationGeoAPI'
    def get(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

    def post(self, name):
        l = Locations.query.filter_by(slug=name).first_or_404()
        if l and request.get_json():
            return request_data_handler(request,self.__name,placeholder=name)
        return {"status":"{0} request payload seems empty, please verify".format(name)}

    def put(self, name):
        l = Locations.query.filter_by(slug=name).first_or_404()
        if l and l.geography:
            return request_data_handler(request,self.__name,placeholder=name)
        return {"status":"{0} geography details not found, add a record with POST".format(name)}

    def delete(self,name):
        l = Locations.query.filter_by(slug=name).first_or_404()
        if l and l.geography:
            return request_data_handler(request,self.__name,placeholder=name)
        return {"status":"{0} geography details not found".format(name)}


#view<endpoint:/location/<name>/stats>
class LocationStatsAPI(MethodView):

    __name = 'LocationStatsAPI'
    def get(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

    def post(self, name):
        l = Locations.query.filter_by(slug=name).first_or_404()
        if l and request.get_json():
            return request_data_handler(request,self.__name,placeholder=name)
        return {"status":"{0} request payload seems empty, please verify".format(name)}

    def put(self, name):
        l = Locations.query.filter_by(slug=name).first_or_404()
        if l and l.stats:
            return request_data_handler(request,self.__name,placeholder=name)
        return {"status":"{0} stats not found, add a record with POST".format(name)}

    def delete(self,name):
        l = Locations.query.filter_by(slug=name).first_or_404()
        if l and l.stats:
            return request_data_handler(request,self.__name,placeholder=name)
        return {"status":"{0} stats not found".format(name)}


#view<endpoint:/location/<name>/pic>
class LocationPicAPI(MethodView):

    __name = 'LocationPicAPI'
    def get(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

    def post(self, name):
        l = Locations.query.filter_by(slug=name).first_or_404()
        if l and request.files:
            return request_data_handler(request,self.__name,placeholder=name)
        return {"status":"{0} request payload seems empty, please verify".format(name)}

    def put(self, name):
        l = Locations.query.filter_by(slug=name).first_or_404()
        if l and request.files:
            return request_data_handler(request,self.__name,placeholder=name)
        return {"status":"{0} record or request payload seems empty, please verify".format(name)}


#view<endpoint:/location/<name>/pic/pic.jpg>
class PicDownloadAPI(MethodView):

    __name = 'PicDownloadAPI'
    def get(self,name,filename):
        location = Locations.query.filter_by(slug=name).first_or_404()
        if location or location.picture :
            return request_data_handler(request,self.__name,placeholder=name,\
                                        pic=filename)

    def delete(self,name,filename):
        location = Locations.query.filter_by(slug=name).first_or_404()
        pic_file = location.picture.picture
        if location and filename == pic_file:
            return request_data_handler(request,self.__name,placeholder=name,\
                                        pic=filename)
        return {"status":"{0} file not found for record {1}({2}) ".format(filename,name,pic_file)}


#view<endpoint:/location/<name>/species>
class LocationSpeciesAPI(MethodView):

    __name = 'LocationSpeciesAPI'
    def get(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

    def post(self, name):
        l = Locations.query.filter_by(slug=name).first_or_404()
        if l and request.get_json():
            return request_data_handler(request,self.__name,placeholder=name)
        return {"status":"{0} species list request payload seems empty, please verify".format(name)}

    def delete(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)


#view<endpoint:/location/<name>/species/<specie_name>
class LocationSpecieAPI(MethodView):

    __name = 'LocationSpecieAPI'
    def get(self,name,specie_name):
        specie = Species.query.filter_by(sp_slug=specie_name).first_or_404()
        if specie:
            return request_data_handler(request,self.__name,\
                                placeholder=name,specie=specie_name)

    def put(self, name,specie_name):
        specie = Species.query.filter_by(sp_slug=specie_name).first_or_404()
        if specie and request.data or request.files:
            return request_data_handler(request,self.__name,\
                                placeholder=name,specie=specie_name)
        return {"status":"{0} specie request payload seems empty, please verify".format(name)}

    def delete(self,name,specie_name):
        specie = Species.query.filter_by(sp_slug=specie_name).first_or_404()
        if specie:
            return request_data_handler(request,self.__name,\
                                    placeholder=name,specie=specie_name)


#view<endpoint:/locations/<name>/species/<specie_name>/<file>.jpg>
class SpeciePicDwnldAPI(MethodView):

    __name = 'SpeciePicDwnldAPI'
    def get(self,name,specie_name,file):
        specie = Species.query.filter_by(pic=file).first_or_404()
        if specie:
            return request_data_handler(request,self.__name,placeholder=name,\
                                        specie=specie_name,pic=file)
    def delete(self,name,specie_name,file):
        specie = Species.query.filter_by(pic=file).first_or_404()
        if specie:
            return request_data_handler(request,self.__name,placeholder=name,\
                                        specie=specie_name,pic=file)
