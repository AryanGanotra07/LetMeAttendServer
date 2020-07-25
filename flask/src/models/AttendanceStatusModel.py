import datetime
from src.extentions import db, bcrypt
import datetime 
from typing import List 


class AttendanceStatusModel(db.Model):
    __tablename__ = "attendancestatusmodel"
    id = db.Column(db.Integer, primary_key=True)
    lect_id = db.Column(db.Integer, db.ForeignKey('lectures.id'))
    sub_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    status = db.Column(db.String(64), nullable = False)
    created_at = db.Column(db.Date, default = datetime.datetime.now().date())
    modified_at = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    at_for = db.Column(db.String)

    def __init__(self,a_for,status):
        self.status = status
        self.at_for = a_for
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_by_sub(cls,sub_id) -> None:
        AttendanceStatusModel.query.filter_by(sub_id = int(sub_id)).delete()
        db.session.commit()
        print("deleted")
    @classmethod
    def delete_by_lect(cls,sub_id) -> None:
        AttendanceStatusModel.query.filter_by(lect_id = int(sub_id)).delete()
        db.session.commit()
        print("deleted")

    @classmethod
    def get_by_lecture_and_date(cls, lect_id, a_for) -> "AttendanceStatusModel":
        return AttendanceStatusModel.query.filter_by(lect_id = lect_id, at_for = a_for).first()
    
    @classmethod
    def get_all(cls, lect_id) -> List['AttendanceStatusModel']:
        return AttendanceStatusModel.query.filter_by(lect_id = lect_id).all()
    @classmethod
    def get_by_id(cls, id) -> "AttendanceStatusModel":
        return AttendanceStatusModel.query.filter_by(id=id).first()