import base
import peewee

''' Define State class, inheriting from peewee BaseModel'''
class State(base.BaseModel):
    name = peewee.CharField(128, null=False, unique=True)
