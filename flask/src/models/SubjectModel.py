import datetime
from src.extentions import db, bcrypt
import datetime
from typing import List
# from src.models.LectureModel import LectureModel


class SubjectModel(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    lectures = db.relationship("LectureModel", backref="subject", lazy='dynamic')
    created_at = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    modified_at = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    # attendance = db.relationship("AttendanceModel", uselist=False, back_populates="subjects")
    # attendance_id = db.Column(db.Integer, db.ForeignKey('attendance.id'))
    current_attendance = db.Column(db.Integer, default = 0)
    total_attendance = db.Column(db.Integer, default = 0)

    def __init__(self, name, color):
        self.name = name
        self.color = color
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def delete(cls,sub_id) -> None:
        SubjectModel.query.filter_by(id = int(sub_id)).delete()
        db.session.commit()
        print("deleted")

    @classmethod
    def get_all(cls, user_id) -> List["SubjectModel"] :
        print("Callsed")
        return SubjectModel.query.filter_by(user_id=user_id).order_by(SubjectModel.created_at.desc()).all()
    
    @classmethod
    def get_subject_by_id(cls, id) -> "SubjectModel":
        return SubjectModel.query.filter_by(id=id).first()
        
