from datetime import datetime
from .database import db

# Locations table: Stores landscape details
class Locations(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    about = db.Column(db.Text, nullable=True)
    datetime = db.Column(db.DateTime, nullable=True,
                              default=datetime.utcnow)

    geographys = db.relationship('Geography', backref='locations',lazy=True, uselist = False)
    statss = db.relationship('Stats', backref='locations', lazy=True, uselist = False)
    flora_faunas = db.relationship('FloraFauna', backref='locations',lazy=True,uselist = False)
    pictures = db.relationship('Pictures', backref='locations',lazy=True,uselist = False)


# Geography table: Stores landscape geographical position and its characters
class Geography(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    lat_long = db.Column(db.String(20), nullable=False)
    climate = db.Column(db.String(20), nullable=True)
    landscape = db.Column(db.String(20), nullable=False)
    locations_id =db.Column(db.Integer, db.ForeignKey('locations.id'),nullable=False)

# Stats table: Stores landscape quantative data
class Stats(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    rank = db.Column(db.Integer, nullable=True)
    stars = db.Column(db.Integer, nullable=True)
    yearly_visitors = db.Column(db.Integer, nullable=True)
    unesco_heritage = db.Column(db.Boolean)
    locations_id =db.Column(db.Integer, db.ForeignKey('locations.id'),nullable=False)

# Flora & Fauna table: Stores landscape biological & botanical information
class FloraFauna(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    species = db.Column(db.Text, nullable=False)
    locations_id =db.Column(db.Integer, db.ForeignKey('locations.id'),nullable=False)

# Pictures table: Stores landscape images file path information
class Pictures(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    pic_path = db.Column(db.String(50), nullable=True)
    locations_id =db.Column(db.Integer, db.ForeignKey('locations.id'),nullable=False)
