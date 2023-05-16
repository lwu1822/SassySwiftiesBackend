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


from flask_cors import CORS
CORS(app)

#comment

""" 
"""

""" 
JWT test
""" 

app.config['SECRET_KEY'] = 'secretkey'

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
            if username is None or len(username) < 2:
                return {'message': f'Username is missing, or is less than 2 characters'}, 400
            # validate uid
           
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

    class _Access(Resource):
        def token_required(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                token = request.args.get('token')

                if not token:
                    return jsonify({'message': 'Token is missing'}), 403

                
                try:
                    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                    #data = jwt.decode(token)
                except:
                    return jsonify({'message': 'Token is invalid'}), 403 
                
                return f(*args, **kwargs)

            return decorated

        @token_required
        def get(self):
            return jsonify({'message': 'Only for people with valid tokens'})


        """ 
        """

    # building RESTapi endpoint
    api.add_resource(_CRUD, '/account')
    api.add_resource(_Security, '/authenticate')
    api.add_resource(_Authentication, '/login')
    api.add_resource(_Access, '/access')
    