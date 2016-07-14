import peewee
import base

''' Define Amenity, inherits from peewee BaseModel '''
class Amenity(base.BaseModel):
    name = peewee.CharField(128, null=False)
