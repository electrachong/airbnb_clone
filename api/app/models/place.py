import peewee
import base
import user, city

''' Define Place class based on peewee BaseModel  '''
class Place(base.BaseModel):
    owner = peewee.ForeignKeyField(user.User, related_name="places")
    city = peewee.ForeignKeyField(city.City, related_name="places")
    name = peewee.CharField(128, null=False)
    description = peewee.TextField()
    number_rooms = peewee.IntegerField(default=0)
    number_bathrooms = peewee.IntegerField(default=0)
    max_guest = peewee.IntegerField(default=0)
    price_by_night = peewee.IntegerField(default=0)
    latitude = peewee.FloatField()
    longitude = peewee.FloatField()
