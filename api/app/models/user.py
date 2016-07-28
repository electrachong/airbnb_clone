import peewee
import hashlib
import base

''' Create a User class inheriting from peewee BaseModel '''
class User(base.BaseModel):
    email = peewee.CharField(128, null=False, unique=True)
    password = peewee.CharField(128, null=False)
    first_name = peewee.CharField(128, null=False)
    last_name = peewee.CharField(128, null=False)
    is_admin = peewee.BooleanField(default=False)

    ''' Store updated password, as a hash '''
    def set_password(self, clear_password):
        m = hashlib.md5()
        m.update(clear_password)
        User.password = m.digest()

    def to_hash(self):
        new_hash = base.BaseModel.to_hash(self)
        new_hash.update(dict(
            email = self.email,
            first_name = self.first_name,
            last_name = self.last_name,
            is_admin = self.is_admin
        ))
        return new_hash

