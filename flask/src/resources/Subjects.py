from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required, get_jwt_claims, create_access_token, create_refresh_token, get_jwt_identity
from src.models.UserModel import UserModel
from src.models.SubjectModel import SubjectModel
from src.schema.SubjectSchema import SubjectSchema
from src.schema.SubjectQuerySchema import SubjectQuerySchema
import datetime
from src.models.LectureModel import LectureModel
import json


subject_schema = SubjectSchema(many = True)
subject_query_schema = SubjectQuerySchema(many = True)
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
        q=request.args.get('q')
        if (q is None and user_id):
            subjects = SubjectModel.get_all(user_id)
            print(subjects)
            return subject_schema.dump(subjects)
        if (q is not None):
            subjects = SubjectModel.get_all_by_name(q, user_id)
            return subject_query_schema.dump(subjects)
    @classmethod
    @jwt_required
    def post(cls):
        user_id = get_jwt_identity()
        json = request.get_json()
        sub=SubjectModel(**json['subject'])
        sub.user_id = user_id
        sub.save_to_db()
        print(sub.id)
        lectureArray = json['lectures']
        for lectureJson in lectureArray:
            lecture = LectureModel(**lectureJson)
            lecture.sub_id = sub.id
            lecture.user_id = user_id
            lecture.save_to_db()
        print(subject_one_schema.dump(sub))
        return subject_one_schema.dump(sub)

        
        

            

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
        LectureModel.delete_by_sub(id)
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

    


