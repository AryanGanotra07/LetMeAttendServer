from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Resource, Api
from src.extentions import bcrypt, db, ma
from flask_cors import CORS
from src.blacklist import BLACKLIST

def create_App():
    app = Flask(__name__)
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
    
