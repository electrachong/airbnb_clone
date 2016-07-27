from flask import Flask
from app import app, json
from app.models.user import User

''' Create a JSON response '''
@app.route('/users', methods=['GET'])
@flask_json.as_json
def index():
        array_users = []
        for user in User.select():
                array_users += user.to_hash()
        return array_users
