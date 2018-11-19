import hashlib

import jwt
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity
from flask_restful import Resource, reqparse

from app import db, marsh
from models.user import User, UserSchema

class GetUserdata(Resource):
    parser = reqparse.RequestParser()

    @jwt_required
    def get(self, userId):
        user = (
			User.query
			.filter(User.userId == userId)
			.one_or_none()
		)
        
        if user is None:
            return { "message": "The specified user does not exist." }, 404

        else:
            userDump = {
                "userId": user.userId,
                "username": user.username,
                # TODO: Country
                # TODO: Club ID
                # TODO: Club Name
                # TODO: Last Login
                # TODO: Current Server,
                # TODO: Coins
                # TODO: Friend Count
                # TODO: Is Member
            }
            
            return userDump