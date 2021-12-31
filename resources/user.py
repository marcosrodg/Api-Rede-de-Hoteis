from flask_jwt_extended.utils import get_jwt
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST


attributes = reqparse.RequestParser()
attributes.add_argument('login',type=str,required=True, help='The field login cannot be empty.')
attributes.add_argument('password',type=str,required=True, help='The field password cannot be empty.')
 

class User(Resource):
   
   # /usuarios/{user_id}
   def get(self,user_id): 
       user = UserModel.find_user(user_id)
       if user:
           return user.json()
       return {'mensage':f'User id {user_id} not found.'}, 404 # Not found
   
   @jwt_required()
   def delete(self,user_id):
        user = UserModel.find_user(user_id)
        if user:
           try:
               user.user_delete()
               return {'mensage':'User deleted successfully'},200 #OK
           except:
               return {'mensage':'An error occurred while deleting user'},500 # Internal Server Error
        return {'mensage': f'User id {user_id} not found.'},404 # Not found
    
    
class UserRegister(Resource):
    
    # /cadastro 
    def post(self):       
        data = attributes.parse_args()
        
        if UserModel.find_by_login(data['login']):
            return {'mensage':f'User login {data["login"]} already exists.'},400 # Bad Request
        
        hash_user = UserModel.get_hash(data['login'],data['password'])
        user = UserModel(data['login'],hash_user)
        try:
            user.save_user()
            return {'mensage':'User created successfully'}, 201 # Created
        except:
            return {'mensage':'An error occurred while saving user'}, 500 # Innternal Server Error
    
class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        data = attributes.parse_args()
        
        user = UserModel.find_by_login(data['login'])
        hash_password = UserModel.get_hash(data['login'],data['password'])
        
        if user and safe_str_cmp(user.password, hash_password):
            access_token = create_access_token(identity=user.user_id)
            return {'access_token':access_token}, 200 # OK
        return {'mensage':'User or password is incorrect'}, 401 #Unauthorized

class UserLogout(Resource):
    
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # JWT Tokenn Idetifier
        BLACKLIST.add(jwt_id)
        return {'mensage':'logged out successfully'},200 #OK