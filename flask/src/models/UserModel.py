import datetime
from flask.src.extentions import db, bcrypt


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    f_name = db.Column(db.String(128), nullable = True)
    l_name = db.Column(db.String(128), nullable = True)
    email = db.Column(db.String(128), unique=True, nullable=True)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now().date())
    modified_at = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    isAdmin = db.Column(db.Boolean, nullable = False, default = False)
    phone = db.Column(db.String(16), nullable = True)

    def __init__(self, username = None, phone = None, email = None, password = None, isAdmin = False):
        self.username = username
        self.phone = phone
        self.email = email
        self.password = self.__generate_hash(password)
        self.isAdmin = isAdmin
    
    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
  
  # add this new method
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)
    


        



