import peewee
import datetime
import sys
# this import statement only works if executing this file in models folder
sys.path.append('../..')
import config

''' Populate peewee database with config variables '''
database = peewee.MySQLDatabase(config.DATABASE['database'], 
                         host=config.DATABASE['host'],
                         port=config.DATABASE['port'],
                         user=config.DATABASE['user'], 
                         passwd=config.DATABASE['password'], 
                         charset=config.DATABASE['charset'])

print database

''' Define the basemodel to be used for peewee classes '''
class BaseModel(peewee.Model):
    id = peewee.PrimaryKeyField(unique=True)
    created_at = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    updated_at = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def save(self, *args, **kwargs):
        # unsure how self.updated_at refers to class variable BaseModel.updated_at
        self.updated_at = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        peewee.Model.save()
    
    class Meta:
        database = database
        order_by = ("id", )
