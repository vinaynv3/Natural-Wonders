from flask_marshmallow import Marshmallow
from flask import current_app
from .models import *


"""
ma : marshmallow,
object serialization/deserialization schema
integrated with Flask-SQLAlchemy models
"""

# Marshmallow database instance
ma = Marshmallow()
def init_marshmallow(app):
    with app.app_context():
        ma.init_app(current_app)


#serializes LocationImage model data
class LocationImageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = LocationImage
        ordered = True
    picture = ma.auto_field()
    _link = ma.URLFor('location', values=dict(name='<locations.slug>'))
    _dwnld = ma.URLFor('dwnld_pic', values=dict(name='<locations.slug>',
                                                filename='<picture>'))


# serializes geography model data
class GeographySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Geography
    lat_long = ma.auto_field()
    climate = ma.auto_field()
    landscape = ma.auto_field()
    _link = ma.URLFor('location', values=dict(name='<locations.slug>'))


# serializes Stats model data
class StatsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Stats
    above_sealevel = ma.auto_field()
    stars = ma.auto_field()
    yearly_visitors = ma.auto_field()
    unesco_heritage = ma.auto_field()
    _link = ma.URLFor('location', values=dict(name='<locations.slug>'))


# serializes Species model data
class SpeciesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Species
        ordered = True
    species_name = ma.auto_field()
    pic = ma.auto_field()
    endangered = ma.auto_field()
    sp_slug = ma.auto_field()
    sp_class = ma.auto_field()
    _specie = ma.URLFor('location_specie', values=dict(name='<locations.slug>',
                                                specie_name='<sp_slug>'))
    _home_link = ma.URLFor('location', values=dict(name='<locations.slug>'))
    _dwnld_pic = ma.URLFor('specie_dwnld_pic', values=dict(name='<locations.slug>',
                                                specie_name='<sp_slug>',
                                                file='<pic>'))


# serializes Location model data
class LocationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Locations
        ordered = True
    #id = ma.auto_field()
    name = ma.auto_field()
    about = ma.auto_field()
    country = ma.auto_field()
    _links = ma.Hyperlinks(
        {
            "_home": ma.URLFor("locations"),
            "geography": ma.URLFor("location_geography", values=dict(name="<slug>")),
            "stats": ma.URLFor("location_stats", values=dict(name="<slug>")),
            "picture":ma.URLFor("location_picture", values=dict(name="<slug>")),
            "species":ma.URLFor("location_species", values=dict(name="<slug>"))
        }
        )


# serializes Locations model data
class LocationsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Locations
        ordered = True
    #id = ma.auto_field()
    name = ma.auto_field()
    about = ma.auto_field()
    country = ma.auto_field()
    _link = ma.URLFor('location', values=dict(name='<slug>'))
    picture = ma.Nested(LocationImageSchema(exclude=['_link']))
    geography = ma.Nested(GeographySchema(exclude=['_link']))
    stats = ma.Nested(StatsSchema(exclude=['_link']))
    species = ma.Nested(SpeciesSchema(exclude=['_home_link'],many=True))
