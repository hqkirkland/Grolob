import enum

from marshmallow_enum import EnumField

from app import db, marsh

class ColorSet(enum.Enum):
    Item = "Item"
    Hair = "Hair"
    Skin = "Skin"

class Color(db.Model):
    __tablename__ = "Colors"
    colorId = db.Column("Id", db.Integer, primary_key=True)
    colorSet = db.Column("ColorSet", db.Enum(ColorSet), nullable=False, default=ColorSet.Item)
    channel1 = db.Column("Channel1", db.BigInteger, nullable=False)
    channel2 = db.Column("Channel2", db.BigInteger, nullable=False)
    channel3 = db.Column("Channel3", db.BigInteger, nullable=False)
    channel4 = db.Column("Channel4", db.BigInteger, nullable=False)

    def __repr__():
        return "<Color %s>" % (colorId)

class ColorSchema(marsh.ModelSchema):
    colorSet = EnumField(ColorSet, by_value=True)
    class Meta:
        model = Color
        ordered = True
        sqla_session = db.session