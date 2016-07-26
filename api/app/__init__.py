from flask import Flask
from flask_json import FlaskJSON

app = Flask(__name__)
json = FlaskJSON(app)

# configure Flask so it will not automatically append status to JSON 
app.config['JSON_ADD_STATUS'] = False

from views import *
