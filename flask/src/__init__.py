from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Resource, Api
from src.extentions import bcrypt, db, ma
from flask_cors import CORS
from src.blacklist import BLACKLIST
from src.resources.User import UserLogin, UserRegister, User
from src.resources.Subjects import Subject, SubjectsList
from src.resources.Lectures import Lecture, LectureList
from dotenv import load_dotenv
import os
from src.config import app_config
import time
import atexit
import requests
import json 
from src.models import UserModel, LectureModel, SubjectModel, AttendanceStatusModel





from apscheduler.schedulers.background import BackgroundScheduler

def send_notif(token):
    url = "https://fcm.googleapis.com/fcm/send"

    payload = "{\n    \"to\":\"fQsrbC_ZRsOlwBrhtRqDPZ:APA91bFw6HranJEzZs0c6Wgf9DktTmBMJhDz8oNq8yZXtuXidQha6-MGDsVBSlyiZ593z0_aGGMF-OHgkkQ5yupCqj3DVTh9PFrztzse7VlUeR3FCis7v2DYJAqvuzUPzKwiugFOuosL\",\n      \"data\":{\"news_id\":\"5e808c920aa62a1dbd6ce3de\"}\n\n}"
    headers = {
    'Authorization': 'key=AAAA8OaMYk4:APA91bHWKNBxtPZ7nCwo1-p2ydPvnRgcgMer76Bzlh94B88I9R5cKpM4LCeJtkQx5qYCTs6Jxkv_74SWqH0h6AV9nhhOjNioKJdTlCnOyicFFkL3LOKDTExgvWG7X8FyrnygCfD-Nzo6',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))

def print_date_time():
    send_notif("cWkPQ8ErQgahXTg1PSSPdl:APA91bGN7AdnxnWHvgh13OZ7WnsSnu_20kjTCvv_e7t6PnrKKyU4IinZCXUetzOltpIGNNLUL2kqT9GJ5qZaHiP8-LeiO__19hsXPlU7FI1yQy50xjKTDvWnYTZVn-5pI42diVz8rguJ")
    

def create_App():
    app = Flask(__name__)
    APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path)
    env_name = os.environ.get('FLASK_ENV')
    app.config.from_object(app_config[env_name])
    api = Api(app)
    jwt = JWTManager(app)
    CORS(app)
    extensions(app)
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(func=print_date_time, trigger="interval", seconds=9)
    # #scheduler.start()
    

    # @jwt.user_claims_loader
    # def add_claims_to_jwt(identity):
    #     from .models.UserModel import UserModel
    #     user = UserModel.find_by_id(identity)
    #     if user.isAdmin:
    #         print("returned is admin as true")
    #         return {'isAdmin' : True}
    #     print("returned is admin as false")
    #     return {'isAdmin' : False}
    #     pass

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        return decrypted_token['jti'] in BLACKLIST

    @jwt.expired_token_loader
    def expired_token_callback():
        return jsonify({
            'description' : 'The token has expired..',
            'error' : 'token_expired'
        }) , 401
    
    @app.route('/')
    def index():
        return "Hello from Aryan", 201
    api.add_resource(UserLogin, '/user/login')
    api.add_resource(UserRegister, '/user/register')
    api.add_resource(User, '/user')
    api.add_resource(Subject, '/subject')
    api.add_resource(SubjectsList, '/subject/all')
    api.add_resource(Lecture, '/lecture/<int:sub_id>')
    api.add_resource(LectureList, '/lecture/all')

    return app

def extensions(app):
  bcrypt.init_app(app) # add this line

  db.init_app(app) # add this line
  
  ma.init_app(app)
  @app.before_first_request
  def create_tables():
    db.create_all()
    # from .models.UserModel import UserModel
    # UserModel.create_admin()
    

app = create_App()
app.app_context().push()
    
