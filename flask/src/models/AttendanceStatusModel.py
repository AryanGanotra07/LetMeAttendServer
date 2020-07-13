import datetime
from src.extentions import db, bcrypt
import datetime 


class AttendanceStatusModel(db.Model):
    __tablename__ = "lectures"
    id = db.Column(db.Integer, primary_key=True)
    lect_id = db.Column(db.String(64), db.ForeignKey('lectures.id'))
    status = db.Column(db.String(64), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now().date())
    modified_at = db.Column(db.DateTime, default = datetime.datetime.utcnow)

    def __init__(self, status):
        self.status = status
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()