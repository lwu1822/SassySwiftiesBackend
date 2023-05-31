import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime as dt

from model.users import User

""" 
JWT test
""" 

from __init__ import app,db  # Definitions initialization
#db.init_app(app)

from flask import jsonify, request, make_response
import jwt 
import datetime 
from functools import wraps

from flask_jwt_extended import (JWTManager, create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, decode_token)

from flask_cors import CORS
CORS(app)

from werkzeug.security import generate_password_hash, check_password_hash

import ast

""" 
"""

""" 
JWT test
""" 

app.config['SECRET_KEY'] = 'secretkey'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_CSRF_CHECK_FORM'] = True

jwt = JWTManager(app)

""" 
""" 

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            username = body.get('username')
            if username is None or len(username) < 1:
                return {'message': f'Username is missing, or is less than 1 characters'}, 400
            # validate username
            dupuser = User.query.filter_by(_username=username).first()
            if dupuser != None and dupuser.username == username:
                print("duplicate")
                return {'message': f'Duplicate Username Detected'}, 400
          
            # look for password and dob
            password = body.get('password')

            ''' #1: Key code block, setup USER OBJECT '''
            uo = User(username=username,
                    password=password)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if password is not None:
                uo.password = password
            # convert to date type
            
    
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {username}, either a format error or username: {username} is duplicate'}, 400

        def get(self): # Read Method
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    

    class _Update(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            username = body.get('username')
            if username is None or len(username) < 1:
                return {'message': f'Username is missing, or is less than 2 characters'}, 400
          
            user = User.query.filter_by(_username=username).first()
            # look for password and dob
            password = body.get('password')

            user = user.update(username, password)

            
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {username}, either a format error or username: {username} is duplicate'}, 400

    class _Delete(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def get(self, username): # Read Method
            user = User.query.filter_by(_username=username).first()
            user.delete()
            return jsonify({"message": "User successfully deleted"})  # jsonify creates Flask response object, more specific to APIs than json.dumps
    
    
    class _Security(Resource):

        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            username = body.get('username')
            if username is None or len(username) < 2:
                return {'message': f'Username is missing, or is less than 2 characters'}, 400
            password = body.get('password')
            
            ''' Find user '''
            user = User.query.filter_by(_username=username).first()
            if user is None or not user.is_password(password):
                return {'message': f"Invalid user id or password"}, 400
            
            ''' authenticated user '''
            return jsonify(user.read())

    class _Authentication(Resource):

        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            username = body.get('username')
            if username is None or len(username) < 1:
                return {'message': f'Username is missing, or is less than 2 characters'}, 400
            password = body.get('password')
            
            ''' Find user '''
            user = User.query.filter_by(_username=username).first()
            if user is None or not user.is_password(password):
                return {'message': f"Invalid user id or password"}, 400

            
            
            token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return jsonify({'token': token})
            
            
            ''' authenticated user '''
            #return jsonify(user.read())
    
    
        """ 
        JWT testing
        """

    class _Login(Resource): # This is currently broken; accepts any set of login credentials. Authentication function is in progress
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            username = body.get('username')
            password = body.get('password')
            
            
            dbUser = User.query.filter_by(_username=username).first()

            
            if dbUser is None:
                return {'message': f"Invalid user id"}, 400

            
            dbUsername = dbUser.username
            dbPassword = dbUser.password

            if not check_password_hash(dbPassword, password):
                return {'message': f"Invalid password"}, 400
            



            access_token = create_access_token(identity=str(username))

            return jsonify( {
                "id": access_token
            })

    class _Info(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            token = body.get('token')
            
            decoded = decode_token(token)

            return jsonify( 
                decoded 
            )
            
            
    class _Output(Resource):
        def get(self):
            myFile = open("api/tsSongInfo.txt", "r")
            fileLine = myFile.readline()
        
            myFile.close()
            
            data = ast.literal_eval(fileLine)
            
            return data
            

    class _UpdateTokens(Resource):
        def put(self):
            body = request.get_json()
            token = body.get('token')

            username = body.get('username')

            user = User.query.filter_by(_username=username).first()
            
            updateToken(self, user, token)
            
            if token_data:
              return token_data

            return {'message': 'placeholder'}

          
          
          #I want to go through the CRUD update function on model. I don't
          #want a blind override here.



        """ 
        """

    

    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')
    api.add_resource(_Authentication, '/access')
    api.add_resource(_Login, '/login')
    api.add_resource(_Info, '/info')
    api.add_resource(_Output, '/output')
    api.add_resource(_Update, '/update')
    api.add_resource(_Delete, '/delete/<username>')
    api.add_resource(_UpdateTokens, '/updateTokens')
    
