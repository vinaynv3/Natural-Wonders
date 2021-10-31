from datetime import datetime
from .database import db
from slugify import slugify
from bisect import bisect

"""
database tables: Locations, LocationImage, Geography, Stats, Species
"""

# Locations table: Stores landscape details
class Locations(db.Model):
    id = db.Column(db.Integer,autoincrement=True, unique=True, primary_key=True)
    name = db.Column(db.String(50),unique=True,nullable=False)
    country = db.Column(db.String(50), nullable=False)
    about = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Database table relationships: one-to-one ('Geography','Stats','LocationImage'), one-to-many('Species)
    picture = db.relationship('LocationImage', backref='locations',uselist=False, lazy=True,
                                        cascade="all, delete", passive_deletes=False)
    geography = db.relationship('Geography', backref='locations',uselist=False,
                                    cascade="all, delete", passive_deletes=False)
    stats = db.relationship('Stats', backref='locations', uselist=False,
                                    cascade="all, delete", passive_deletes=False)
    species = db.relationship('Species', backref='locations', uselist=True,
                                    cascade="all, delete", passive_deletes=False)

    #constructor
    def __init__(self,data:dict):
        try:
            self.name = data.get('name',' ')
            self.country = data.get('country',' ')
            self.about = data.get('about',' ')
            self.slug = slugify(data.get('name',' '))
        except ValueError as e:
            raise ValueError('<{0} {1}>'.format(self.__class__,str(e)))
        except TypeError as e:
            raise TypeError('<{0} {1}>'.format(self.__class__,str(e)))

    def __repr__(self):
        return '<Locations ({0},{1})>'.format(self.name,self.id)


#Location picture
class LocationImage(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    picture = db.Column(db.String(50),unique=True, nullable=False)
    locations_id =db.Column(db.Integer, db.ForeignKey('locations.id',ondelete='CASCADE')
                                ,nullable=False,unique=True)

    #constructor
    def __init__(self,file_name:str,locations=None):
        if locations:
            try:
                self.picture = file_name
                self.locations = locations
            except ValueError as e:
                raise ValueError('<{0} {1}>'.format(self.__class__,str(e)))
            except TypeError as e:
                raise TypeError('<{0} {1}>'.format(self.__class__,str(e)))

        else:
            raise Exception('<{0} missing fk for field locations>'.format(self.__class__))

    def __repr__(self):
        return '<LocationImage ({0},{1},{2})>'.format(self.picture,self.locations.name,self.locations_id)


# Geography table: Stores landscape geographical position and its characters
class Geography(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    lat_long = db.Column(db.String(20), nullable=True)
    climate = db.Column(db.String(20), nullable=False)
    landscape = db.Column(db.String(20), nullable=False)
    locations_id =db.Column(db.Integer, db.ForeignKey('locations.id',ondelete='CASCADE')
                                ,nullable=False,unique=True)

    #constructor
    def __init__(self,data:dict,locations=None):
        if locations:
            try:
                self.lat_long = data.get('lat_long',' ')
                self.climate = data.get('climate',' ')
                self.landscape = data.get('landscape',' ')
                self.locations = locations
            except ValueError as e:
                raise ValueError('<{0} {1}>'.format(self.__class__,str(e)))
            except TypeError as e:
                raise TypeError('<{0} {1}>'.format(self.__class__,str(e)))

        else:
            raise Exception('<{0} missing fk for field locations>'.format(self.__class__))

    def __repr__(self):
        return '<Geography ({0},{1},{2})>'.format(self.landscape,self.locations.name,self.id)


# Stats table: Stores landscape quantative data
class Stats(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    above_sealevel = db.Column(db.Integer, nullable=True,default=0)
    stars = db.Column(db.Integer, nullable=True,default=0)
    yearly_visitors = db.Column(db.Integer, nullable=True,default=0)
    unesco_heritage = db.Column(db.Boolean,nullable=False, default=False)
    locations_id =db.Column(db.Integer, db.ForeignKey('locations.id',ondelete='CASCADE')
                                        ,unique=True,nullable=False)

    #constructor
    def __init__(self,data:dict,locations=None):
        if locations:
            try:
                self.yearly_visitors = int(data.get('yearly_visitors',0))
                self.stars = 1 if int(data.get('stars',0))>0  else 0
                self.unesco_heritage = bool(data.get('unesco_heritage',0))
                self.above_sealevel = int(data.get('above_sealevel',0))
                self.locations = locations
            except ValueError as e:
                raise ValueError('<{0} {1}>'.format(self.__class__,str(e)))
            except TypeError as e:
                raise  TypeError('<{0} {1}>'.format(self.__class__,str(e)))

        else:
            raise Exception('<{0} missing fk for field locations>'.format(self.__class__))

    def __repr__(self):
        return '<Stats ({0},{1},{2})>'.format(self.yearly_visitors,self.locations.name,self.id)


# Species table: Stores landscape biological & botanical information
class Species(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    species_name = db.Column(db.String(30), nullable=False)
    pic = db.Column(db.String(50), nullable=True)
    endangered = db.Column(db.Boolean,nullable=True, default=False)
    sp_slug = db.Column(db.String(30), nullable=False)
    sp_class = db.Column(db.String(30), nullable=True)
    locations_id =db.Column(db.Integer, db.ForeignKey('locations.id',ondelete='CASCADE')
                                ,nullable=False)

    #constructor
    def __init__(self,data:dict,locations=None):
        if locations:
            try:
                self.species_name = data.get('species_name',' ')
                self.endangered = bool(data.get('endangered',0))
                self.sp_slug = slugify(data.get('species_name',' '))
                self.sp_class = data.get('sp_class',' ')
                self.locations = locations
            except ValueError as e:
                raise ValueError('<{0} {1}>'.format(self.__class__,str(e)))
            except TypeError as e:
                raise TypeError('<{0} {1}>'.format(self.__class__,str(e)))

        else:
            raise Exception('<{0} missing fk for field locations>'.format(self.__class__))

    def __repr__(self):
        return '<Species ({0},{1},{2})>'.format(self.species_name,self.locations.name,self.locations_id)
