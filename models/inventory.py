import enum

from marshmallow_enum import EnumField

from app import db, marsh
from models.game_item import GameItem
from models.item_type import ItemType
from models.single_enum import SingleEnum
from models.user import User

class Inventory(db.Model):
    __tablename__ = "Inventory"
    entryId = db.Column("Id", db.Integer, primary_key=True)
    userId = db.Column("UserId", db.Integer, db.ForeignKey('User.Id'))
    gameItemId = db.Column("GameItemId", db.Integer, db.ForeignKey('GameItem.Id'))
    colorId = db.Column("ColorId", db.Integer, db.ForeignKey('Color.Id'))

class InventorySchema(marsh.ModelSchema):
    class Meta:
        model = Inventory
        ordered = True
        sqla_session = db.session