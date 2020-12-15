import hashlib
import random

import jwt
from flask.views import MethodView
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity
from webargs import fields
from webargs.flaskparser import use_args

from app import db

from models.user import User, UserSchema
from models.betaticket import BetaTicket, BetaTicketSchema

user_schema = UserSchema(many=False)

class Authorize(MethodView):
	@use_args({"username": fields.Str(required=True), "password": fields.Str(required=True)}, location="json")
	def post(self, args):
		print(args)
		loginVars = args
		user = (
			User.query
			.filter((User.username == loginVars["username"]) | (User.email == loginVars["username"]))
			.filter(User.password == hashlib.sha256(str(loginVars["password"]).encode('utf-8')).hexdigest().upper())
			.one_or_none()
		)

		if user is None:
			return {
				"message": "The username or password is invalid." 
				}, 401
		
		else:
			SEGMENT_A = "CLOUDSPIRE"
			SEGMENT_B = "MEYANJUNGLE"
			SEGMENT_C = "MISTYISLAND"
			SEGMENT_D = range(0,9)

			key1 = "%s%s%s%s" % (random.choice(SEGMENT_A), random.choice(SEGMENT_B), random.choice(SEGMENT_D), random.choice(SEGMENT_C))
			key2 = "%s%s%s%s" % (random.choice(SEGMENT_B), random.choice(SEGMENT_D), random.choice(SEGMENT_C), random.choice(SEGMENT_A))
			key3 = "%s%s%s%s" % (random.choice(SEGMENT_C), random.choice(SEGMENT_A), random.choice(SEGMENT_B), random.choice(SEGMENT_D))

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