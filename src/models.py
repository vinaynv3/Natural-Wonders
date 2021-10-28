from datetime import datetime
from .database import db
from slugify import slugify


# Locations table: Stores landscape details
class Locations(db.Model):
    id = db.Column(db.Integer,autoincrement=True, unique=True, primary_key=True)
    name = db.Column(db.String(50),unique=True,nullable=False)
    country = db.Column(db.String(50), nullable=False)
    about = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True,
                              default=datetime.utcnow)

    # Database table relationships: one-to-one ('Geography','Stats','LocationImage'), one-to-many('Species)
    picture = db.relationship('LocationImage', backref='locations',uselist=False,
                                        cascade="all, delete", passive_deletes=False)
    geography = db.relationship('Geography', backref='locations',uselist=False,
                                    cascade="all, delete", passive_deletes=False)
    stats = db.relationship('Stats', backref='locations', uselist=False,
                                    cascade="all, delete", passive_deletes=False)
    species = db.relationship('Species', backref='locations', uselist=True,
                                    cascade="all, delete", passive_deletes=False)

    #constructor
    def __init__(self,data:dict):
        self.name = data['name']
        self.country = data['country']
        self.about = data['about']
        self.slug = slugify(data['name'])

    def __repr__(self):
        return '<Locations ({0},{1})>'.format(self.name,self.id)

#Location picture
class LocationImage(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    picture = db.Column(db.String(50), nullable=False)
    locations_id =db.Column(db.Integer, db.ForeignKey('locations.id',ondelete='CASCADE')
                                ,nullable=False,unique=True)

    #constructor
    def __init__(self,data:dict,locations=None):
        if locations:
            self.picture = data['file_name']
            self.locations = locations
        else:
            raise Exception('<{0} missing fk for field locations>'.format(self.__class__))

    def __repr__(self):
        return '<Species ({0},{1},{2})>'.format(self.species_name,self.locations.name,self.locations_id)



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
            self.lat_long = data['lat_long']
            self.climate = data['climate']
            self.landscape = data['landscape']
            self.locations = locations
        else:
            raise Exception('<{0} missing fk for field locations>'.format(self.__class__))

    def __repr__(self):
        return '<Geography ({0},{1},{2})>'.format(self.landscape,self.locations.name,self.id)


# Stats table: Stores landscape quantative data
class Stats(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    rank = db.Column(db.Integer, nullable=True)
    stars = db.Column(db.Integer, nullable=True)
    yearly_visitors = db.Column(db.Integer, nullable=True)
    unesco_heritage = db.Column(db.Boolean, default=False)
    locations_id =db.Column(db.Integer, db.ForeignKey('locations.id',ondelete='CASCADE')
                                        ,unique=True,nullable=False)

    #constructor
    def __init__(self,data:dict,locations=None):
        if locations:
            self.stars = 1 if data['stars'] else 0
            self.rank = Locations.query.count()
            self.unesco_heritage = bool(data['unesco_heritage'])
            self.yearly_visitors = int(data['yearly_visitors'])
            self.locations = locations
        else:
            raise Exception('<{0} missing fk for field locations>'.format(self.__class__))

    def __repr__(self):
        return '<Stats ({0},{1},{2})>'.format(self.yearly_visitors,self.locations.name,self.id)


# Species table: Stores landscape biological & botanical information
class Species(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    species_name = db.Column(db.String(50), nullable=False)
    locations_id =db.Column(db.Integer, db.ForeignKey('locations.id',ondelete='CASCADE')
                                ,nullable=False)

    #constructor
    def __init__(self,data:dict,locations=None):
        if locations:
            self.species_name = data['species_name']
            self.locations = locations
        else:
            raise Exception('<{0} missing fk for field locations>'.format(self.__class__))

    def __repr__(self):
        return '<Species ({0},{1},{2})>'.format(self.species_name,self.locations.name,self.locations_id)
