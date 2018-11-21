import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from config import mariadb_connection_string, secret_session_key

basedir = os.path.abspath(os.path.dirname(__file__))

# Initiate app + settings
app = Flask(__name__)
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = mariadb_connection_string
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_SECRET_KEY'] = secret_session_key

# Initiate data access and schemas
api = Api(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)
marsh = Marshmallow(app)
migrate = Migrate(app, db)

from authentication import Authorize
from userdata import GetUserdata
from gamedata import ListColors, ListItems

# Register endpoints
api.add_resource(Authorize, '/auth/signin')
api.add_resource(GetUserdata, '/userdata/<int:userId>')
api.add_resource(ListColors, '/gamedata/colors')
api.add_resource(ListItems, '/gamedata/itemdata/<string:item_type>')
# Setup