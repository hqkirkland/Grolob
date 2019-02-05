import hashlib
import random

import jwt
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity
from flask_restful import Resource, reqparse

from app import db, marsh
from models.user import User, UserSchema
from models.betaticket import BetaTicket, BetaTicketSchema

user_schema = UserSchema(many=False)
ticket_schema = BetaTicketSchema(many=False)

class GetUserdata(Resource):
    parser = reqparse.RequestParser()

    @jwt_required
    def get(self, user_id):
        user = (
			User.query
			.filter(User.userId == user_id)
			.one_or_none()
		)
        
        if user is None:
            return { "message": "The specified user does not exist." }, 404
        
        else:
            user_dump = user_schema.dump(user).data
            return user_dump
        
class IssueTicket(Resource):
    parser = reqparse.RequestParser()

    def get(self):
        SEQUENCE_A = "CLOUDSPIRE"
        SEQUENCE_B = "MEYANJUNGLE"
        SEQUENCE_C = "MISTYISLAND"
        SEQUENCE_D = range(0,9)

        key1 = "%s%s%s%s" % (random.choice(SEQUENCE_A), random.choice(SEQUENCE_B), random.choice(SEQUENCE_D), random.choice(SEQUENCE_C))
        key2 = "%s%s%s%s" % (random.choice(SEQUENCE_B), random.choice(SEQUENCE_D), random.choice(SEQUENCE_C), random.choice(SEQUENCE_A))
        key3 = "%s%s%s%s" % (random.choice(SEQUENCE_C), random.choice(SEQUENCE_A), random.choice(SEQUENCE_B), random.choice(SEQUENCE_D))

        serial = ("%s-%s-%s") % (key1, key2, key3)
        ticket = BetaTicket()
        ticket.serialKey = serial
        ticket.issued = True

        db.session.add(ticket)
        db.session.commit()

        return ticket_schema.dump(ticket).data