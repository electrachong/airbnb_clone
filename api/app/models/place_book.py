import peewee
import datetime
import base
import place, user

''' Define PlaceBook, inherits from peewee BaseModel '''
class PlaceBook(base.BaseModel):
    place = peewee.ForeignKeyField(place.Place)
    user = peewee.ForeignKeyField(user.User, related_name = "places_booked")
    is_validated = peewee.BooleanField(default=False)
    date_start = peewee.DateTimeField(null=False)
    number_nights = peewee.IntegerField(default=1)
