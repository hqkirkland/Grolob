from app import db, marsh

class User(db.Model):
    __tablename__ = "User"
    userId = db.Column("Id", db.Integer, primary_key=True)
    username = db.Column("Username",db.String(16), nullable=False)
    password = db.Column("Password", db.String(64), nullable=False)
    email = db.Column("Email", db.String(255), nullable=False)
    appearance = db.Column("Appearance", db.String(72), nullable=False)

    def __repr__():
        return "<User %s>" % (username)

class UserSchema(marsh.ModelSchema):
    class Meta:
        model = User
        exclude = ('password', 'email')
        ordered = True
        sqla_session = db.session