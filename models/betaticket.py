from app import db, marsh

class BetaTicket(db.Model):
    __tablename__ = "BetaTickets"
    ticketId = db.Column("Id", db.Integer, primary_key=True)
    serialKey = db.Column("SerialKey", db.String(14), nullable=False)
    issued = db.Column("Issued", db.Boolean, nullable=False, default=False)

    def __repr__():
        return "<Ticket %s>" % (serialKey)

class BetaTicketSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = BetaTicket
        ordered = True
        sqla_session = db.session
        load_instance = True