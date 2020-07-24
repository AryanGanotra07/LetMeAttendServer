
from src.models.LectureModel import LectureModel
from src.models.SubjectModel import SubjectModel
from src.models.AttendanceStatusModel import AttendanceStatusModel
from flask_restful import Resource, request, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

class AttendanceStatus(Resource):
    
    @classmethod
    @jwt_required
    def post(cls, lect_id):
        data = request.get_json()
        a_s = AttendanceStatusModel(**data)
        a_s.lect_id = lect_id
        a_s.save_to_db()
        print(data)
        return {"message":"Attendance marked"}
        pass
    @classmethod
    @jwt_required
    def get(cls, lect_id):
        #get all status of a lect_id
        pass
    
    @classmethod
    @jwt_required
    def put(cls, lect_id):
        pass
