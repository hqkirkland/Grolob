import hashlib

import jwt
from flask import Flask, request, jsonify
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
        return color_schema.dump(colors)

class ListItems(MethodView):
    def get(self, item_type):
        item_list = []
        
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

        for item in item_set:
            item_row = (
                item.gameItemId,
                item.itemType.value,
                item.itemName,
                item.description,
                item.layered.value
            )

            item_list.append(item_row)
            
        return item_list