
from src.models.LectureModel import LectureModel
from src.models.SubjectModel import SubjectModel
from src.models.AttendanceStatusModel import AttendanceStatusModel
from src.schema.AttendanceStatusSchema import AttendanceStatusSchema
from flask_restful import Resource, request, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

schema = AttendanceStatusSchema()
many_schema = AttendanceStatusSchema(many=True)

class AttendanceStatus(Resource):
    
    @classmethod
    @jwt_required
    def post(cls, lect_id):
        data = request.get_json()
        a_for = data['a_for']
        if (AttendanceStatusModel.get_by_lecture_and_date(lect_id, a_for) is not None):
            return {"message" : "Attendance already marked"}
        a_s = AttendanceStatusModel(**data)
        a_s.lect_id = lect_id
        
        lecture = LectureModel.get_lecture_by_id(lect_id)
        lecture.sent = False
        date_time_obj = datetime.datetime.strptime(a_for, '%d/%m/%Y')
        lecture.last_marked = date_time_obj
        lecture.save_to_db()
        subject = SubjectModel.get_subject_by_id(lecture.sub_id)
        a_s.sub_id = subject.id
        a_s.save_to_db()
        status = data['status']
        if (status == 'yes'):
            subject.current_attendance += 1
            subject.total_attendance+=1
            subject.save_to_db()
        elif (status == 'no'):
            subject.total_attendance+=1
            subject.save_to_db()
        elif (status == 'cancel'):
            pass
        print(data)
        return {"message":"Attendance marked"}
        pass
    @classmethod
    @jwt_required
    def get(cls, lect_id):
        #get all status of a lect_id
        statuses = AttendanceStatusModel.get_all(lect_id)
        return many_schema.dump(statuses)
        
    
    @classmethod
    @jwt_required
    def put(cls, lect_id):
        data = request.get_json()
        # a_for = data['at_for']
        print(data)
        a_s = AttendanceStatusModel.get_by_id(data['id'])
        
        subject = SubjectModel.get_subject_by_id(a_s.sub_id)
        status = data['status']
        if (status == 'yes' and a_s.status == 'no'):
            subject.current_attendance += 1
            # subject.total_attendance+=1
        
        elif (status == 'yes' and a_s.status == 'cancel'):
            subject.total_attendance+=1
            subject.current_attendance += 1
            
        elif (status == 'cancel' and a_s.status == 'yes'):
            subject.total_attendance-=1
            subject.current_attendance-=1
        elif (status == 'cancel' and a_s.status == 'no'):
            subject.total_attendance-=1
        elif (status == 'no' and a_s.status == 'yes'):
            subject.current_attendance-=1
        elif (status == 'no' and a_s.status == 'cancel'):
            subject.total_attendance+=1
        subject.save_to_db()  
        a_s.status = status
        a_s.save_to_db()
        print(data)
        return schema.dump(a_s)
        pass
