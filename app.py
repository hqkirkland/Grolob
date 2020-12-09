import os

from flask import Flask, send_from_directory
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

from config import mariadb_connection_string, secret_session_key

# Initiate app + settings
app = Flask(__name__, static_url_path='')
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = mariadb_connection_string
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_SECRET_KEY'] = secret_session_key

@app.route("/")
def hello():
    return "Welcome to Dreamland! It's not ready for you yet, though :-)\n \"Stay tuned!\""

@app.route('/Hadley/<path:path>')
def send_js(path):
    if (path == ""):
        return send_from_directory('Hadley', 'index.html')
    else:
        return send_from_directory('Hadley', path)

# Initiate data access and schemas
api = Api(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)
marsh = Marshmallow(app)

from authentication import Authorize
from userdata import GetUserdata, CreatePlayer, IssueTicket, GetInventory
from gamedata import ListColors, ListItems

# Register endpoints
api.add_resource(Authorize, '/auth/signin')
api.add_resource(GetUserdata, '/userdata/<int:user_id>')
api.add_resource(IssueTicket, '/userdata/issueticket')
api.add_resource(CreatePlayer, '/userdata/createplayer')
api.add_resource(ListColors, '/gamedata/colors')
api.add_resource(ListItems, '/gamedata/itemdata/<string:item_type>')
api.add_resource(GetInventory, '/userdata/inventory/<int:user_id>')
# Setup
