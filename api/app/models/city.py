import peewee
import base
import state

''' Define class City, inherits peewee BaseModel '''
class City(base.BaseModel):
    name = peewee.CharField(128, null=False)
    state = peewee.ForeignKeyField(state.State, related_name="cities", on_delete="CASCADE")
