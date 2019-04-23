import hashlib

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
			access_token = create_access_token(identity=user.userId, fresh=True)
			refresh_token = create_refresh_token(user.userId)
			return {
				"userId": user.userId,
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