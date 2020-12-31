import os

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

from config import mariadb_connection_string, secret_session_key

# Initiate app + settings
app = Flask(__name__, static_url_path="")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = mariadb_connection_string
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = secret_session_key

@app.route("/")
def hello():
    return "Welcome to Dreamland! It's not ready for you yet, though :-)\n \"Stay tuned!\""

@app.route("/Hadley/<path:path>")
def send_js(path):
    if (path == ""):
        return send_from_directory("Hadley", "index.html")
    else:
        return send_from_directory("Hadley", path)

# Initiate data access and schemas
db = SQLAlchemy(app)
db.init_app(app)
db.create_all()

jwt = JWTManager(app)
marsh = Marshmallow(app)

from authentication import Authorize
from userdata import GetUserdata, CreatePlayer, IssueTicket, GetInventory
from gamedata import ListColors, ListItems

# Register endpoints
# 'Get' implies single
# 'List' implies many
app.add_url_rule("/auth/signin", view_func=Authorize.as_view("authorize"))
app.add_url_rule("/userdata/<int:user_id>", view_func=GetUserdata.as_view("user_get_data"))
app.add_url_rule("/userdata/issueticket", view_func=IssueTicket.as_view("user_issue_ticket"))
app.add_url_rule("/userdata/createplayer", view_func=CreatePlayer.as_view("user_create_player"))
app.add_url_rule("/userdata/inventory/<int:user_id>", view_func=GetInventory.as_view("user_inventory"))
app.add_url_rule("/gamedata/colors", view_func=ListColors.as_view("gamedata_colors"))
app.add_url_rule("/gamedata/itemdata/<string:item_type>", view_func=ListItems.as_view("gamedata_items"))
# app.add_url_rule("/gamedata/itemdata/<int:item_gameitemid>", view_func=GetItemData.as_view("gamedata_itemdata"))

# Setup