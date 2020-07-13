import datetime
from src.extentions import db, bcrypt
import datetime
from typing import List


class SubjectModel(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    lectures = db.relationship("Lecture", backref="subject", lazy='dynamic')
    created_at = db.Column(db.DateTime, default = datetime.datetime.now().date())
    modified_at = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    attendance = db.relationship("attendance", uselist=False, back_populates="subjects")

    def __init__(self, name, color):
        self.name = name
        self.color = color
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls, user_id) -> List["SubjectModel"] :
        return SubjectModel.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_subject_by_id(cls, id) -> "SubjectModel":
        return SubjectModel.query.filter_by(id=id).first()
        
