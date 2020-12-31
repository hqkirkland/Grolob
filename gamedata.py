import hashlib

import jwt
from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity
from flask.views import MethodView
from app import db, marsh

from models.color import Color, ColorSchema
from models.game_item import GameItem, GameItemSchema
from models.item_type import ItemType

color_schema = ColorSchema(many=True)
item_schema = GameItemSchema(many=False)
item_multi_schema = GameItemSchema(many=True)

class ListColors(MethodView):
    def get(self):
        colors = Color.query.all()
        result_set = color_schema.jsonify(colors)
        
        return make_response(result_set, 200)

class ListItems(MethodView):
    def get(self, item_type):
        
        if item_type == "all":
            item_set = (
                GameItem.query
                .all()
            )
        
        elif item_type in [option.value.lower() for option in ItemType]:
            item_set = (
                GameItem.query
                .filter(GameItem.itemType == item_type)
                .filter(GameItem.available)
                .all()
            )

        else:
            return { "message": "Could not locate any items of that type." }, 404
        
        result_set = item_multi_schema.jsonify(item_set)
        return make_response(result_set, 200)