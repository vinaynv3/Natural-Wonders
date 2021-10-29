
import os
from flask.views import MethodView
from .models import *
from .serializer import *
from flask import request, current_app, send_from_directory,redirect, url_for
from .helpers import request_data_handler, database_session
from werkzeug.utils import secure_filename



class IndexAPI(MethodView):

    def get(self):
        return {'natural_wonders':'http://api.naturalwonders.com/',
                'locations':'http://api.naturalwonders.com/locations/',
                'location_name':'http://api.naturalwonders.com/locations/<name>/',
                'location_images':'http://api.naturalwonders.com/locations/image/<name>/',
                }


class LocationsAPI(MethodView):

    __name = 'LocationsAPI'
    def get(self):
        locations = Locations.query.all()
        locations_schema = LocationsSchema(many=True)
        data = dict(natural_wonders=locations_schema.dump(locations),
                    total=len(locations))
        return data

    def post(self,*args,**kwargs):
        return request_data_handler(request.get_json(),self.__name)


class LocationAPI(MethodView):

    __name = 'LocationAPI'

    def get(self,name):
        location = Locations.query.filter_by(slug=name).first_or_404()
        location_schema = LocationSchema()
        data = location_schema.dump(location)
        return data

    def post(self,name):
        return {'status' :'requested http method not allowed for corresponding endpoint'}

    def put(self, name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request.get_json(),self.__name,placeholder=name)

    def delete(self,name):
        if Locations.query.filter_by(slug=name).first_or_404():
            return request_data_handler(request.get_json(),self.__name,placeholder=name,delete=True)


class LocationImageAPI(MethodView):

    """
             **********LocationImageAPI: location image management tool**********
    class is designed to handle only one image per location, http methods below outlines the
    implementation and images are found under folder app/media/
    GET: image can be accessed only if image already present in database
    POST: creates new image record in model LocationImage relative to endpoint /locations/<name>/
    PUT: updates image record in model LocationImage relative to endpoint /locations/<name>/
    DELETE: deletes image record in model LocationImage & upload folder relative to endpoint /locations/<name>/
    """
    def location_attr(self,name):
        location = Locations.query.filter_by(slug=name).first_or_404()
        return location

    def get(self,name):
        loc_image = LocationImage.query.filter_by(locations=self.location_attr(name)).first_or_404()
        if loc_image:
            return send_from_directory(current_app.config["UPLOAD_FOLDER"], loc_image.picture)


    def allowed_file(self,filename):
        return '.' in filename and \
                   filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

    def remove_file(self,filename):
        folder = current_app.config['UPLOAD_FOLDER']
        for filename.picture in os.listdir(folder):
            file_path = os.path.join(folder, filename.picture)
            try:
                os.remove(file_path)
                database_session(filename,delete=True)
                return True
            except Exception as e:
                return False

    def post(self,name):

        f = list(request.files.keys())[0]
        file = request.files[f]
        if f not in request.files or file.filename == '':
            return {'status':'missing file in content type header for record {0}'.format(name)}

        elif file and self.allowed_file(file.filename) and not self.location_attr(name).picture:
            filename = secure_filename(file.filename)
            database_session(LocationImage(filename,locations=self.location_attr(name)))
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('location_picture', name=name,_method='GET'))
        else:
            return {'status':'{0} file already created for record {1}'.format(file,name)}

    def put(self, name):
        f = list(request.files.keys())[0]
        file = request.files[f]
        if f not in request.files or file.filename == '':
            return {'status':'missing file in content type header for record {0}'.format(name)}
        elif file and self.allowed_file(file.filename) and self.location_attr(name).picture:
            picture_model = LocationImage.query.filter_by(locations=self.location_attr(name)).first_or_404()
            status = self.remove_file(picture_model)
            filename = secure_filename(file.filename)
            database_session(LocationImage(filename,locations=self.location_attr(name)))
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('location_picture', name=name,_method='GET'))
        else:
            return {'status':'{0} file doesnt exist for record {1} to update'.format(file,name)}

    def delete(self,name):

        if self.location_attr(name).picture:
            filename = LocationImage.query.filter_by(locations=self.location_attr(name)).first_or_404()
            if self.remove_file(filename):
                return {'status':'{0} deleted for record {1}'.format(filename.picture,name)}
        else:
            f = list(request.files.keys())[0]
            file = request.files[f]
            return {'status':'{0} file doesnt exist for record {1} to delete'.format(file,name)}
