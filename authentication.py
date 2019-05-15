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

class Authorize(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument("username", type=str, required=True)
	parser.add_argument("password", type=str, required=True)

	def post(self):
		login = self.parser.parse_args()
		user = (
			User.query
			.filter((User.username == login["username"]) | (User.email == login["username"]))
			.filter(User.password == hashlib.sha256(str(login["password"]).encode('utf-8')).hexdigest())
			.one_or_none()
		)

		if user is None:
			return {
				"message": "The username or password is invalid." 
				}, 401
		
		else:
			SEQUENCE_A = "CLOUDSPIRE"
			SEQUENCE_B = "MEYANJUNGLE"
			SEQUENCE_C = "MISTYISLAND"
			SEQUENCE_D = range(0,9)

			key1 = "%s%s%s%s" % (random.choice(SEQUENCE_A), random.choice(SEQUENCE_B), random.choice(SEQUENCE_D), random.choice(SEQUENCE_C))
			key2 = "%s%s%s%s" % (random.choice(SEQUENCE_B), random.choice(SEQUENCE_D), random.choice(SEQUENCE_C), random.choice(SEQUENCE_A))
			key3 = "%s%s%s%s" % (random.choice(SEQUENCE_C), random.choice(SEQUENCE_A), random.choice(SEQUENCE_B), random.choice(SEQUENCE_D))

			game_ticket = ("%s-%s-%s") % (key1, key2, key3)

			access_token = create_access_token(identity=user.userId, fresh=True)
			refresh_token = create_refresh_token(user.userId)
			user.gameTicket = game_ticket

			db.session.add(user)
			db.session.commit()
			
			return {
				"userId": user.userId,
				"gameTicket": user.gameTicket,
				"access_token": access_token, 
				"refresh_token": refresh_token
				}, 200
	
	@jwt_refresh_token_required
	def get(self):
		user = get_jwt_identity()
        # Return non-fresh token for the user
		new_token = create_access_token(identity=user, fresh=False)
		return {
			"access_token": new_token 
			}, 200