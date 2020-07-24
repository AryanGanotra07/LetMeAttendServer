from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required, get_jwt_claims, create_access_token, create_refresh_token, get_jwt_identity
from src.models.UserModel import UserModel
import datetime

# user_schema = UserSchema()
# user_many_schema = UserSchema(many = True)
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('id', 
    type = str, 
    required = True,
    help = "This field cannot be blank")
_user_parser.add_argument('token', 
    type = str, 
    required = True,
    help = "This field cannot be blank")
# _user_parser.add_argument('email', 
#     type = str, 
#     required = False,
#     help = "This field can be blank for login")
class UserLogin(Resource):
    @classmethod
    def get(cls):
        pass

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
       
        if user and user.check_hash(data['password']):
            print(1)
            expires = datetime.timedelta(days=1)
            access_token = create_access_token(identity=user.id, fresh = True,expires_delta=expires)
            print(2)
            refresh_token = create_refresh_token(user.id)
            print(3)
            # recents = UserModel.get_recent_accounts()
            return {
                'access_token' : access_token,
                'refresh_token' : refresh_token,
                'id' : user.id,
               

            }, 201
            print(4)
        return {'message' : 'Return invalid credentials'}, 401

class UserRegister(Resource):
    @classmethod
    # @jwt_required
    def post(cls):
        # claims = get_jwt_claims()
        # if not claims['isAdmin']:
        #      return {'message' : 'Admin priviledge required'} , 401
        data = _user_parser.parse_args()
        print(data)
        from src.resources.Task import execute
        execute()
        
        # user = user_schema.load(data)
        user = UserModel.find_by_id(data['id'])
        if user is None:
            user = UserModel(**data)
            user.save_to_db()

        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=user.id, fresh = True,expires_delta=expires)
        refresh_token = create_refresh_token(user.id)
        # recents = UserModel.get_recent_accounts()
        return {
            'access_token' : access_token,
            'refresh_token' : refresh_token,
        }, 201
    
class User(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        data = request.get_json()
        print(data)
        attendanceCriteria = data['attendanceCriteria']
        if(attendanceCriteria is None):
            return {"status" : 0, "message" : "Missing attribute - attendanceCriteria"}
        user_id = get_jwt_identity()
        if (user_id is None):
            return {"status" : 0, "message" : "No user found"}
        user = UserModel.find_by_id(user_id)
        if user is None:
            return {"status" : 0, "message" : "No user found"}
        user.attendanceCriteria = attendanceCriteria
        user.save_to_db()
        return {"status" : 1, "message" : "Attendance field successfully added"}
    
    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        if (user_id is None):
            return {"status" : 0, "message" : "No user found"}
        user = UserModel.find_by_id(user_id)
        if user is None:
            return {"status" : 0, "message" : "No user found"}
        return {"attendanceCriteria" : user.attendanceCriteria} 
        

        


    