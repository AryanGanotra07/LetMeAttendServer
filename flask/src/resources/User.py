from flask import Resource
from flask_jwt_extended import jwt_required, get_jwt_claims

class UserLogin(Resource):
    @classmethod
    def post(cls):
        pass

    @classmethod
    @jwt_required
    def get(cls):
        claims = get_jwt_claims()
        if not claims['isAdmin']:
            return {'message' : 'Admin priviledge required'} , 401
        return {"message" : "Authenticated"} , 201


    