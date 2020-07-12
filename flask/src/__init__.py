from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Resource, Api
from src.extentions import bcrypt, db, ma
from flask_cors import CORS
from src.blacklist import BLACKLIST
from src.resources.User import UserLogin, UserRegister
from dotenv import load_dotenv
import os
from src.config import app_config

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
    

    @jwt.user_claims_loader
    def add_claims_to_jwt(identity):
        from .models.UserModel import UserModel
        user = UserModel.find_by_id(identity)
        if user.isAdmin:
            print("returned is admin as true")
            return {'isAdmin' : True}
        print("returned is admin as false")
        return {'isAdmin' : False}
        pass

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
    
