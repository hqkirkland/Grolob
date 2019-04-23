import hashlib
import random

import jwt
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity
from flask_restful import Resource, reqparse
from webargs import fields
from webargs.flaskparser import use_args

from app import db, marsh
from models.user import User, UserSchema
from models.betaticket import BetaTicket, BetaTicketSchema

user_schema = UserSchema(many=False)
ticket_schema = BetaTicketSchema(many=False)

class GetUserdata(Resource):
    # Need to remove parser in favor of webargs.
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

class CreatePlayer(Resource):
    def post(self):
        args = request.get_json(force=True)
        username = args["username"].strip()
        password = args["password"].strip()
        email_address = args["email"].strip()
        appearance = args["appearance"].strip()
        alphakey = args["alphakey"].strip()
        
        # Check if username is taken.
        user = (
			User.query
			.filter(User.email == email_address)
			.one_or_none()
		)
        
        # Check if email is taken.
        if user is None:
            user = (
                User.query
                .filter(User.username == username)
                .one_or_none()
            )

        if user is not None:
            return { "message": "The specified user already exists! " }, 400

        else:
            user = User()
            user.username = username
            user.email = email_address
            user.password = password
            user.appearance = appearance
            user.gameTicket = alphakey

        ticket = (
            BetaTicket.query
            .filter(BetaTicket.serialKey == alphakey)
            .filter(BetaTicket.issued == True)
            .one_or_none()
        )

        if ticket is None:
            return { "message": "The given game ticket key is invalid." }, 404
        
        db.session.delete(ticket)
        db.session.commit()

        db.session.add(user)
        db.session.commit()
        
        return { "message": "Registration successful!", 200 }
