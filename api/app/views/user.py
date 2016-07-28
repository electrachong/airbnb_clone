from flask import request
from app import app, json
from app.models.user import User
import peewee
import flask_json

''' Create a JSON response '''
@app.route('/users', methods=['GET'])
@flask_json.as_json
def get_user():
        array_users = []
        for user in User.select():
                array_users += user.to_hash()
        return array_users

@app.route('/users', methods=['POST'])
@flask_json.as_json
def create_user():

        # for now, we are going to validate our data up-front
        ''' another method would be to catch peewee exceptions 
            (e.g. OperationalError: (1048, "Column 'is_admin' cannot be null")) 
            and this might save some work, but it's an open question as to what 
            is better practice '''
        post_param = dict(
                email = request.form.get("email"),
                password = request.form.get("password"),
                first_name = request.form.get("first_name"),
                last_name = request.form.get("last_name"),
                is_admin = request.form.get("is_admin")
        )

        # If any required parameters are missing:
        '''if post_param['email'] == None \
           or post_param['password'] == None \
           or post_param['first_name'] == None \
           or post_param['last_name'] == None:
                return dict(
                        code=400,
                        msg="Bad request: missing data"
                ), 400'''

        ''' If is_admin is not specified, set its value to the default (False), 
            otherwise cast it to Boolean so the proper type is passed '''
        if post_param['is_admin'] == True \
           or post_param['is_admin'] == False:
                post_param['is_admin'] = Boolean(post_param['is_admin'])
        else:
                post_param['is_admin'] = False

        try:
                new_user = User(
                        email = post_param['email'],
                        password = post_param['password'],
                        first_name = post_param['first_name'],
                        last_name = post_param['last_name'],
                        is_admin = post_param['is_admin']
                )
                new_user.set_password(new_user.password)
                new_user.save()
        except peewee.OperationalError:
                return dict(
                        code=400,
                        msg="Bad request: missing data"
                ), 400
        except peewee.IntegrityError:
                return dict(
                        code=10000,
                        msg="Email already exists"
                ), 409
