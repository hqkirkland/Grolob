from app import db, marsh

class User(db.Model):
    __tablename__ = "User"
    userId = db.Column("Id", db.Integer, primary_key=True)
    username = db.Column("Username",db.String(16))
    password = db.Column("Password", db.String(64))
    email = db.Column("Email", db.String(255))

    def __repr__():
        return "<User %s>" % (username)

class UserSchema(marsh.ModelSchema):
    class Meta:
        model = User
        ordered = True
        sqla_session = db.session