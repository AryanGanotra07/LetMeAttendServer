import datetime
from src.extentions import db, bcrypt
import datetime 


class AttendanceModel(db.Model):
    __tablename__ = "attendance"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    current_attendance = db.Column(db.Integer, nullable = False)
    total_attendance = db.Column(db.Integer, nullable = False)
    subject = db.relationship("subjects", uselist=False, back_populates="attendance")
    created_at = db.Column(db.DateTime, default = datetime.datetime.now().date())
    modified_at = db.Column(db.DateTime, default = datetime.datetime.utcnow)

    def __init__(self, status):
        self.status = status
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()