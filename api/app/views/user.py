from flask import request, jsonify
from app import app
from app.models.user import User
import index
import peewee
import flask_json

# Return a list of Users in JSON format to GET requests
@app.route('/users', methods=['GET'])
def get_user():
        array_users = []
        for user in User.select():
                array_users += [user.to_hash()]
        return jsonify(array_users)

# Create a new User record using POST parameter data
# Return JSON response with User info if successfully created
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

        # Create new User record using Peewee module class
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
        ''' Deal with exception if a required field was null
            by returning 400 response '''
        except peewee.OperationalError:
                return dict(
                        code=400,
                        msg="Bad request: missing data"
                ), 400
        # Deal with exception that arises if email was not unique
        except peewee.IntegrityError:
                return dict(
                        code=10000,
                        msg="Email already exists"
                ), 409

        return new_user.to_hash()

''' Retrieve appropriate user and return JSON response
    with the correct information '''
@app.route('/users/<user_id>', methods=['GET'])
@flask_json.as_json
def get_user_by_id(user_id):

        # Use Peewee to retrieve User record as Python obj
        try:
                selected_user = User.get(User.id == user_id)
                return selected_user.to_hash()
        # Send 404 response if requested record does not exist
        except User.DoesNotExist:
                return index.not_found()

