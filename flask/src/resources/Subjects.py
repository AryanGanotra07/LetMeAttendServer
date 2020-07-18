from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required, get_jwt_claims, create_access_token, create_refresh_token, get_jwt_identity
from src.models.UserModel import UserModel
from src.models.SubjectModel import SubjectModel
from src.schema.SubjectSchema import SubjectSchema
import datetime


subject_schema = SubjectSchema(many = True)
subject_one_schema = SubjectSchema()
_subject_parser = reqparse.RequestParser()
_subject_parser.add_argument('name', 
    type = str, 
    required = True,
    help = "This field cannot be blank")
_subject_parser.add_argument('color', 
    type = str, 
    required = True,
    help = "This field cannot be blank")
_subject_parser.add_argument('id', 
    type = str, 
    required = False,
   )

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
        subject = SubjectModel(name = data['name'], color = data['color'])
        if (user_id and subject):
            user = UserModel.find_by_id(user_id)
            if user:
                subject.user_id = user_id
                subject.save_to_db()
                # user.subjects.append(subject)
                return subject_one_schema.dump(subject)
            return {"message" : "User not found", "status" : 0}

        return {"message" : "User not found or error in creating subject", "status" : 0}
        
    
    @classmethod
    def get(cls, id):
        #getSubjectDetails
        pass
    
    @classmethod
    @jwt_required
    def delete(cls):
        id = request.get_json()
        print(id)
        SubjectModel.delete(id)
        return {"message" : "subject deleted successfully"}, 201
    
    @classmethod
    @jwt_required
    def put(cls):
        data = _subject_parser.parse_args()
        # user_id = get_jwt_identity()
        # print(user_id)
        subject = SubjectModel.get_subject_by_id(data['id'])
        if (subject):
            if(data['name']):
                subject.name = data['name']
            subject.save_to_db()
            # user = UserModel.find_by_id(user_id)
            # if user:
            #     subject.user_id = user_id
            #     subject.save_to_db()
            #     # user.subjects.append(subject)
            return subject_one_schema.dump(subject)

        return {"message" : "User not found or error in creating subject", "status" : 0}

    


