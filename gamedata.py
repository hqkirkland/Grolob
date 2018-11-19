import hashlib

import jwt
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity
from flask_restful import Resource, reqparse

from app import db, marsh
from models.colors import Color, ColorSchema

color_schema = ColorSchema(many=True)

class ListColors(Resource):
    def get(self):
        colors = Color.query.all()
        return color_schema.dump(colors).data
#class ListServers(Resource):
    #parser = reqparse.RequestParser()
	#parser.add_argument("", type=str, required=True)