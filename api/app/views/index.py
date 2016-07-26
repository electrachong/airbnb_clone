from flask import Flask
import datetime
import peewee
import flask_json
from app import app, json
from app.models.base import database

''' Create a JSON response '''
@app.route('/', methods=['GET'])
@flask_json.as_json
def index():
    return dict(status="OK", utc_time=datetime.datetime.utcnow(), time=datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

''' Connect to the database before every request '''
@app.before_request
def before_request():
    database.connect()

''' Close the database connection after every request '''
@app.after_request
def after_request(response):
    database.close()
    return response

''' In case of 404 error, return JSON with a not found message '''
@app.errorhandler(404)
@flask_json.as_json
def not_found(self):
    return dict(code=404, msg="not found"), 404
