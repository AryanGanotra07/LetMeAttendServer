from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required, get_jwt_claims, create_access_token, create_refresh_token, get_jwt_identity
from src.models.UserModel import UserModel
from src.models.LectureModel import LectureModel
from src.models.SubjectModel import SubjectModel
from src.schema.LectureSchema import LectureSchema
from src.models.AttendanceStatusModel import AttendanceStatusModel
import datetime

lecture_one_schema = LectureSchema()
lecture_schema = LectureSchema(many = True)
_lecture_parser = reqparse.RequestParser()
# _lecture_parser.add_argument('name', 
#     type = str, 
#     required = True,
#     help = "This field cannot be blank")
# _lecture_parser.add_argument('color', 
#     type = str, 
#     required = True,
#     help = "This field cannot be blank")
_lecture_parser.add_argument('end_time', 
type = str, 
required = True,
help = "This field cannot be blank")
_lecture_parser.add_argument('start_time', 
    type = str, 
    required = True,
    help = "This field cannot be blank")
_lecture_parser.add_argument('day', 
    type = int, 
    required = True,
    help = "This field cannot be blank")


class LectureList(Resource):
    # @jwt_required
    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        # if (user_id):
        day=request.args.get('day')
        sub_id = request.args.get('sub_id')
        if(day and day=='today'):
            lectures = LectureModel.get_today_lectures(user_id)
        elif (day and day in ["0","1","2","3","4","5","6"]):
            print("Called")
            lectures = LectureModel.get_lectures_by_day(user_id,day)
        elif (sub_id):
            lectures = LectureModel.get_all(sub_id)
        else:
            lectures = LectureModel.get_all_by_user(user_id)
        print(lectures)
        return lecture_schema.dump(lectures)
        

class Lecture(Resource):
    @classmethod
    @jwt_required
    def post(cls, sub_id):
        data = request.get_json()
        user_id = get_jwt_identity()
        print(user_id)
        lecture = LectureModel(**data)
        if (user_id and lecture):
            user = UserModel.find_by_id(user_id)
            if user:
                lecture.user_id = user_id
                lecture.sub_id = sub_id
                lecture.save_to_db()
                # user.subjects.append(subject)
                return lecture_one_schema.dump(lecture)
            return {"message" : "User not found", "status" : 0}

        return {"message" : "User not found or error in creating lecture", "status" : 0}
        
    
    @classmethod
    def get(cls, id):
        #getSubjectDetails
        pass

    @classmethod
    @jwt_required
    def delete(cls,sub_id):
        id = request.get_json()
        print(id)
        statuses = AttendanceStatusModel.get_all(id)
        if (len(statuses) > 0):
            f_status = statuses[0]
            subject = SubjectModel.get_subject_by_id(f_status.sub_id)
            for status in statuses:
                if (status.status == 'yes'):
                    subject.current_attendance-=1
                    subject.total_attendance-=1
                    subject.save_to_db()
                elif status.status == 'no':
                    subject.total_attendance-=1
                    subject.save_to_db()
                    pass
                elif status.status == 'cancel':
                    pass
        AttendanceStatusModel.delete_by_lect(id)
        LectureModel.delete(id)
        return {"message" : "lecture deleted successfully"}, 201
    
    @classmethod
    @jwt_required
    def put(cls, sub_id):
        data = request.get_json()
        print(data)
        # user_id = get_jwt_identity()
        # print(user_id)
        lecture = LectureModel.get_lecture_by_id(data['id'])
        if (lecture):
            if(data['start_time']):
                lecture.start_time = data['start_time']
            if(data['end_time']):
                lecture.end_time = data['end_time']
            lecture.save_to_db()
            # user = UserModel.find_by_id(user_id)
            # if user:
            #     lecture.user_id = user_id
            #     lecture.save_to_db()
            #     # user.lectures.append(lecture)
            return lecture_one_schema.dump(lecture)

        return {"message" : "User not found or error in creating subject", "status" : 0}
    


