from flask import request, jsonify
from app import app
from app.models.user import User
import peewee
import flask_json

''' Specify responses for /users route '''
@app.route('/users', methods=['GET'])
def get_user():
        array_users = []
        for user in User.select():
                array_users += [user.to_hash()]
        return jsonify(array_users)

@app.route('/users', methods=['POST'])
@flask_json.as_json
def create_user():

        is_admin = request.form.get("is_admin")

        ''' If is_admin is not specified, set its value to the default (False), 
            otherwise cast it to Boolean so the proper type is passed '''
        if is_admin == True \
           or is_admin == False:
                is_admin = Boolean(is_admin)
        else:
                is_admin = False

        # Note: right now, this does not prevent empty strings being passed to API
        try:
                new_user = User(
                        email = request.form.get('email'),
                        password = request.form.get('password'),
                        first_name = request.form.get('first_name'),
                        last_name = request.form.get('last_name'),
                        is_admin = is_admin
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
