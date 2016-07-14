from flask import Flask
from flask_json import FlaskJSON

app = Flask(__name__)
json = FlaskJSON(app)

# update if needed:
from views import *
from models import *
