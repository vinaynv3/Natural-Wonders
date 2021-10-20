from datetime import datetime
from .database import db


# Locations table: Stores landscape details
class Locations(db.Model):
    id = db.Column(db.Integer,autoincrement=True, unique=True, primary_key=True)
    name = db.Column(db.String(50),unique=True,nullable=False)
    country = db.Column(db.String(50), nullable=False)
    about = db.Column(db.Text, nullable=False)
    pic = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), nullable=False)
    datetime = db.Column(db.DateTime, nullable=True,
                              default=datetime.utcnow)

    # Database table relationships: one-to-one ('Geography','Stats'), one-to-many('Species)
    geography = db.relationship('Geography', backref='locations',uselist=False,
                                    cascade="all, delete", passive_deletes=False)
    stats = db.relationship('Stats', backref='locations', uselist=False,
                                    cascade="all, delete", passive_deletes=False)
    species = db.relationship('Species', backref='locations', uselist=True,
                                    cascade="all, delete", passive_deletes=False)

    def __repr__(self):
        return '<Locations ({0},{1})>'.format(self.name,self.id)


# Geography table: Stores landscape geographical position and its characters
class Geography(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    lat_long = db.Column(db.String(20), nullable=True)
    climate = db.Column(db.String(20), nullable=False)
    landscape = db.Column(db.String(20), nullable=False)
    locations_id =db.Column(db.Integer, db.ForeignKey('locations.id',ondelete='CASCADE')
                                ,nullable=False,unique=True)

    def __repr__(self):
        return '<Geography ({0},{1},{2})>'.format(self.landscape,self.locations.name,self.id)


# Stats table: Stores landscape quantative data
class Stats(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    rank = db.Column(db.Integer, nullable=True)
    stars = db.Column(db.Integer, nullable=True)
    yearly_visitors = db.Column(db.Integer, nullable=True)
    unesco_heritage = db.Column(db.Boolean)
    locations_id =db.Column(db.Integer, db.ForeignKey('locations.id',ondelete='CASCADE')
                                        ,unique=True,nullable=False)

    def __repr__(self):
        return '<Stats ({0},{1},{2})>'.format(self.yearly_visitors,self.locations.name,self.id)


# Species table: Stores landscape biological & botanical information
class Species(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    species_name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(50), nullable=True)
    locations_id =db.Column(db.Integer, db.ForeignKey('locations.id',ondelete='CASCADE')
                                ,nullable=False)

    def __repr__(self):
        return '<Species ({0},{1},{2})>'.format(self.species_name,self.locations.name,self.locations_id)
