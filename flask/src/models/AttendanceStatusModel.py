import datetime
from src.extentions import db, bcrypt
import datetime 


class AttendanceStatusModel(db.Model):
    __tablename__ = "attendancestatusmodel"
    id = db.Column(db.Integer, primary_key=True)
    lect_id = db.Column(db.Integer, db.ForeignKey('lectures.id'))
    status = db.Column(db.String(64), nullable = False)
    created_at = db.Column(db.Date, default = datetime.datetime.now().date())
    modified_at = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    a_for = db.Column(db.String)

    def __init__(self,a_for,status):
        self.status = status
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()