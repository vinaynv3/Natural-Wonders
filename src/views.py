
import os
import json
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

#view<endpoint:/location/>
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


#view<endpoint:/location/<name>/>
class LocationAPI(MethodView):

    __name = 'LocationAPI'
    def get(self,name):
        return request_data_handler(request,self.__name,placeholder=name)

    def put(self, name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

    def delete(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)


#view<endpoint:/location/<name>/geo/>
class LocationGeoAPI(MethodView):

    __name = 'LocationGeoAPI'
    def get(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

    def post(self, name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

    def put(self, name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

    def delete(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)


#view<endpoint:/location/<name>/stats/>
class LocationStatsAPI(MethodView):

    __name = 'LocationStatsAPI'
    def get(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

    def post(self, name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

    def put(self, name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

    def delete(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)


#view<endpoint:/location/<name>/pic/>
class LocationPicAPI(MethodView):

    __name = 'LocationPicAPI'
    def get(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

    def post(self, name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

    def put(self, name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

    def delete(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

#view<endpoint:/location/<name>/pic/pic.jpg>
class PicDownloadAPI(MethodView):

    __name = 'PicDownloadAPI'
    def get(self,name,filename):
        location = Locations.query.filter_by(slug=name).first_or_404()
        if location and location.picture :
            return request_data_handler(request,self.__name,placeholder=name,\
                                        pic=filename)


#view<endpoint:/location/<name>/species/>
class LocationSpeciesAPI(MethodView):

    __name = 'LocationSpeciesAPI'
    def get(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

    def post(self, name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)

    def delete(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,placeholder=name)


#view<endpoint:/location/<name>/species/<specie_name>/
class LocationSpecieAPI(MethodView):

    __name = 'LocationSpecieAPI'
    def get(self,name,specie_name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,\
                                placeholder=name,specie=specie_name)

    def put(self, name,specie_name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,\
                                placeholder=name,specie=specie_name)

    def delete(self,name,specie_name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request,self.__name,\
                                    placeholder=name,specie=specie_name)
