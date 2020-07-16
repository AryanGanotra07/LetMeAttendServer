from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, create_access_token, create_refresh_token, get_jwt_identity
from src.models.UserModel import UserModel
from src.models.SubjectModel import SubjectModel
from src.schema.SubjectSchema import SubjectSchema
import datetime

subject_schema = SubjectSchema(many = True)
_subject_parser = reqparse.RequestParser()
_subject_parser.add_argument('name', 
    type = str, 
    required = True,
    help = "This field cannot be blank")
_subject_parser.add_argument('color', 
    type = str, 
    required = True,
    help = "This field cannot be blank")

class SubjectsList(Resource):
    # @jwt_required
    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        if (user_id):
            subjects = SubjectModel.get_all(user_id)
            print(subjects)
            return subject_schema.dump(subjects)
            

class Subject(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        data = _subject_parser.parse_args()
        user_id = get_jwt_identity()
        print(user_id)
        subject = SubjectModel(**data)
        if (user_id and subject):
            user = UserModel.find_by_id(user_id)
            if user:
                subject.user_id = user_id
                subject.save_to_db()
                # user.subjects.append(subject)
                return {"message" : "Subject successfully saved", "status" : 1}
            return {"message" : "User not found", "status" : 0}

        return {"message" : "User not found or error in creating subject", "status" : 0}
        
    
    @classmethod
    def get(cls, id):
        #getSubjectDetails
        pass
    


