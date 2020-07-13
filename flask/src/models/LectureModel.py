import datetime
from src.extentions import db, bcrypt
import datetime 


class LectureModel(db.Model):
    __tablename__ = "lectures"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    attendanceStatuses = db.relationship("AttendanceStatus", backref="lecture", lazy='dynamic')
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    sub_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    start_time = db.Column(db.DateTime, default = datetime.datetime.time)
    end_time = db.Column(db.DateTime, default = datetime.datetime.time)
    day = db.Column(db.DateTime, default = datetime.datetime.day)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now().date())
    modified_at = db.Column(db.DateTime, default = datetime.datetime.utcnow)

    def __init__(self, name, color, start_time, end_time, day):
        self.name = name
        self.color = color
        self.start_time = start_time
        self.end_time = end_time
        self.day = day
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
