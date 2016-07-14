import peewee
import base

''' Define class PlaceAmenities -- inherits from peewee Model  '''
class PlaceAmenities(peewee.Model):
    place = peewee.ForeignKeyField(Place)
    amenity = peewee.ForeignKeyField(Amenity)

    class Meta:
        database = base.database
