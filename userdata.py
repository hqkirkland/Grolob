import hashlib

import jwt
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity
from flask_restful import Resource, reqparse

from app import db, marsh
from models.user import User, UserSchema

user_schema = UserSchema(many=False)

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