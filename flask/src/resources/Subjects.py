from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, create_access_token, create_refresh_token, get_jwt_identity
from src.models.UserModel import UserModel
from src.models.SubjectModel import SubjectModel
import datetime

class SubjectsList(Resource):
    # @jwt_required
    @classmethod
    def get(cls):
        user_id = get_jwt_identity()
        if (user_id):
            subjects = SubjectModel.get_all()
            return {
                'subjects': subjects
            }

class Subject(Resource):
    @classmethod
    def post(cls):
        #adding subject
        pass
    
    @classmethod
    def get(cls, id):
        #getSubjectDetails
        pass
    
    

