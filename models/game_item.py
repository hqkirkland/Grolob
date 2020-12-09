import enum

from marshmallow_enum import EnumField

from app import db, marsh
from models.item_type import ItemType
from models.single_enum import SingleEnum

class GameItem(db.Model):
    __tablename__ = "GameItem"
    gameItemId = db.Column("Id", db.Integer, primary_key=True)
    itemType = db.Column("ItemType", db.Enum(ItemType), nullable=False, default=ItemType.Collectible)
    itemName = db.Column("ItemName", db.String(36), nullable=False, default="?")
    setId = db.Column("SetId", db.Integer, nullable=True, default="0")
    description = db.Column("Description", db.String(255), nullable=False, default="This item seems broken; perhaps a High Monk should look into it..")
    layered = db.Column("Layered", db.Enum(SingleEnum), nullable=False, default=SingleEnum.N)
    cost = db.Column("Cost", db.Integer, nullable=True, default=5)
    sale = db.Column("Sale", db.Integer, nullable=True, default=0)
    available = db.Column("Available", db.Boolean, nullable=False, default=True)
    membersOnly = db.Column("MembersOnly", db.Boolean, nullable=False, default=False)

    def __repr__():
        return "<GameItem %s>" % (gameItemId)

class GameItemSchema(marsh.ModelSchema):
    itemType = EnumField(ItemType, by_value=True)
    layered = EnumField(SingleEnum, by_value=True)

    class Meta:
        model = GameItem
        ordered = True
        sqla_session = db.session