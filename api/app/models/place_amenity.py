import peewee
import base
import place, amenity

''' Define class PlaceAmenities -- inherits from peewee Model  '''
class PlaceAmenities(peewee.Model):
    place = peewee.ForeignKeyField(place.Place)
    amenity = peewee.ForeignKeyField(amenity.Amenity)

    class Meta:
        database = base.database
