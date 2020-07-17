import datetime
from src.extentions import db, bcrypt
import datetime 
from typing import List 


class LectureModel(db.Model):
    __tablename__ = "lectures"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    attendanceStatuses = db.relationship("AttendanceStatusModel", backref="lecture", lazy='dynamic')
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    sub_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    start_time = db.Column(db.String(20), default = datetime.datetime.now().strftime('%H:%M:%S'))
    end_time = db.Column(db.String(20), default = datetime.datetime.now().strftime('%H:%M:%S'))
    day = db.Column(db.Integer, default = datetime.datetime.weekday)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now().date())
    modified_at = db.Column(db.DateTime, default = datetime.datetime.utcnow)

    def __init__(self,name, color, start_time, end_time, day):
        self.name = name
        self.color = color
        self.start_time = start_time
        self.end_time = end_time
        self.day = day
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_all(cls, sub_id) -> List["LectureModel"] :
        return LectureModel.query.filter_by(sub_id=sub_id).all()
    
    @classmethod
    def get_lecture_by_id(cls, id) -> "LectureModel":
        return LectureModel.query.filter_by(id=id).first()
    
    @classmethod
    def get_today_lectures(cls, user_id) -> List["LectureModel"]:
        weekday = datetime.datetime.today().weekday()
        print(weekday)
        return LectureModel.query.filter_by(user_id=user_id,day=weekday).all()

    @classmethod
    def get_lectures_by_day(cls,user_id,day)-> List["LectureModel"]:
        return LectureModel.query.filter_by(user_id=user_id,day=day).all()
    
    @classmethod
    def get_all_by_user(cls, user_id)-> List["LectureModel"] :
        return LectureModel.query.filter_by(user_id=user_id).all()
    


        
