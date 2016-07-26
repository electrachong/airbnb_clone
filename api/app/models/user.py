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
        return dict(
            id = User.id,
            created_at = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            updated_at = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            email = User.email,
            first_name = User.first_name,
            last_name = User.last_name,
            is_admin = User.is_admin
        )

