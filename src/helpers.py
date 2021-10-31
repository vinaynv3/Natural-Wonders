from .database import db
from flask import current_app,send_from_directory
from werkzeug.utils import secure_filename
import os

# database session handler
def database_session(model,insert=False,delete=False):
    try:
        storage = db.session
        if insert:
            storage.add(model)
        elif delete:
            storage.delete(model)
        else:
            return
    finally:
        storage.commit()
        storage.close()


# allowed files png', 'jpg', 'jpeg', 'gif'
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

#file validator
def validate_file(files,f):
    if f not in files or files[f].filename == '':
        return False
    return True

#saves media file into folder ../media/
def save_file(files,model,location,slug,picture=False):
    f = list(files.keys())[0]
    file = files.get(f,0)
    if validate_file(files,f):
        filename = secure_filename(file.filename)
        database_session(model(filename,locations=location),insert=True)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return True
    return {'status':'{0} file already created for record {1}'.format(file.filename,slug)}



#displays media file from folder ../media/ for download
def download_file(picture):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], picture.picture)

#removes media file from folder ../media/
def delete_file(picture):
    folder = current_app.config['UPLOAD_FOLDER']
    if picture.picture in os.listdir(folder):
        file_path = os.path.join(folder,picture.picture)
        os.remove(file_path)
        database_session(picture,delete=True)
        return True
    return False
