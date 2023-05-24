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

#comment

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
            if username is None or len(username) < 2:
                return {'message': f'Username is missing, or is less than 2 characters'}, 400
            # validate username
            #dupuser = User.query.filter_by(_username=username)
            #if dupuser
              #return {'message': f'Duplicate Username Detected'}, 400
          
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

    class _Login(Resource): # This is currently broken; accepts any set of login credentials. Authentication function is in progress
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            username = body.get('username')
            password = body.get('password')
            
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
            return jsonify({'status': True, 'albums': {'totalCount': 23, 'items': [{'type': 'album', 'id': '3lS1y25WAhcqJDATJK70Mq', 'name': 'Midnights (3am Edition)', 'shareUrl': 'https://open.spotify.com/album/3lS1y25WAhcqJDATJK70Mq', 'date': '2022-10-22T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e02e0b60c608586d88252b8fbc0', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d00004851e0b60c608586d88252b8fbc0', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b273e0b60c608586d88252b8fbc0', 'width': 640, 'height': 640}], 'trackCount': 20}, {'type': 'album', 'id': '151w1FgRZfnKZA9FEcg9Z3', 'name': 'Midnights', 'shareUrl': 'https://open.spotify.com/album/151w1FgRZfnKZA9FEcg9Z3', 'date': '2022-10-21T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e02bb54dde68cd23e2a268ae0f5', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d00004851bb54dde68cd23e2a268ae0f5', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b273bb54dde68cd23e2a268ae0f5', 'width': 640, 'height': 640}], 'trackCount': 13}, {'type': 'album', 'id': '6kZ42qRrzov54LcAk4onW9', 'name': "Red (Taylor's Version)", 'shareUrl': 'https://open.spotify.com/album/6kZ42qRrzov54LcAk4onW9', 'date': '2021-11-12T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e02318443aab3531a0558e79a4d', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d00004851318443aab3531a0558e79a4d', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b273318443aab3531a0558e79a4d', 'width': 640, 'height': 640}], 'trackCount': 30}, {'type': 'album', 'id': '4hDok0OAJd57SGIT8xuWJH', 'name': "Fearless (Taylor's Version)", 'shareUrl': 'https://open.spotify.com/album/4hDok0OAJd57SGIT8xuWJH', 'date': '2021-04-09T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e02a48964b5d9a3d6968ae3e0de', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d00004851a48964b5d9a3d6968ae3e0de', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b273a48964b5d9a3d6968ae3e0de', 'width': 640, 'height': 640}], 'trackCount': 26}, {'type': 'album', 'id': '6AORtDjduMM3bupSWzbTSG', 'name': 'evermore (deluxe version)', 'shareUrl': 'https://open.spotify.com/album/6AORtDjduMM3bupSWzbTSG', 'date': '2021-01-07T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e0290fd9741e1838115cd90b3b6', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d0000485190fd9741e1838115cd90b3b6', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b27390fd9741e1838115cd90b3b6', 'width': 640, 'height': 640}], 'trackCount': 17}, {'type': 'album', 'id': '2Xoteh7uEpea4TohMxjtaq', 'name': 'evermore', 'shareUrl': 'https://open.spotify.com/album/2Xoteh7uEpea4TohMxjtaq', 'date': '2020-12-11T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e0233b8541201f1ef38941024be', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d0000485133b8541201f1ef38941024be', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b27333b8541201f1ef38941024be', 'width': 640, 'height': 640}], 'trackCount': 15}, {'type': 'album', 'id': '0PZ7lAru5FDFHuirTkWe9Z', 'name': 'folklore: the long pond studio sessions (from the Disney+ special) [deluxe edition]', 'shareUrl': 'https://open.spotify.com/album/0PZ7lAru5FDFHuirTkWe9Z', 'date': '2020-11-25T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e02045514e3ed4e1767a7c3ece5', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d00004851045514e3ed4e1767a7c3ece5', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b273045514e3ed4e1767a7c3ece5', 'width': 640, 'height': 640}], 'trackCount': 34}, {'type': 'album', 'id': '1pzvBxYgT6OVwJLtHkrdQK', 'name': 'folklore (deluxe version)', 'shareUrl': 'https://open.spotify.com/album/1pzvBxYgT6OVwJLtHkrdQK', 'date': '2020-08-18T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e02c288028c2592f400dd0b9233', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d00004851c288028c2592f400dd0b9233', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b273c288028c2592f400dd0b9233', 'width': 640, 'height': 640}], 'trackCount': 17}, {'type': 'album', 'id': '2fenSS68JI1h4Fo296JfGr', 'name': 'folklore', 'shareUrl': 'https://open.spotify.com/album/2fenSS68JI1h4Fo296JfGr', 'date': '2020-07-24T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e0295f754318336a07e85ec59bc', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d0000485195f754318336a07e85ec59bc', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b27395f754318336a07e85ec59bc', 'width': 640, 'height': 640}], 'trackCount': 16}, {'type': 'album', 'id': '1NAmidJlEaVgA3MpcPFYGq', 'name': 'Lover', 'shareUrl': 'https://open.spotify.com/album/1NAmidJlEaVgA3MpcPFYGq', 'date': '2019-08-23T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e02e787cffec20aa2a396a61647', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d00004851e787cffec20aa2a396a61647', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b273e787cffec20aa2a396a61647', 'width': 640, 'height': 640}], 'trackCount': 18}, {'type': 'album', 'id': '6DEjYFkNZh67HP7R9PSZvv', 'name': 'reputation', 'shareUrl': 'https://open.spotify.com/album/6DEjYFkNZh67HP7R9PSZvv', 'date': '2017-11-10T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e02da5d5aeeabacacc1263c0f4b', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d00004851da5d5aeeabacacc1263c0f4b', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b273da5d5aeeabacacc1263c0f4b', 'width': 640, 'height': 640}], 'trackCount': 15}, {'type': 'album', 'id': '1MPAXuTVL2Ej5x0JHiSPq8', 'name': 'reputation Stadium Tour Surprise Song Playlist', 'shareUrl': 'https://open.spotify.com/album/1MPAXuTVL2Ej5x0JHiSPq8', 'date': '2017-11-09T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e0263d77f99117b28af9f656918', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d0000485163d77f99117b28af9f656918', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b27363d77f99117b28af9f656918', 'width': 640, 'height': 640}], 'trackCount': 46}, {'type': 'album', 'id': '34OkZVpuzBa9y40DCy0LPR', 'name': '1989 (Deluxe Edition)', 'shareUrl': 'https://open.spotify.com/album/34OkZVpuzBa9y40DCy0LPR', 'date': '2014-10-27T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e02332d85510aba3eb28312cfb2', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d00004851332d85510aba3eb28312cfb2', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b273332d85510aba3eb28312cfb2', 'width': 640, 'height': 640}], 'trackCount': 19}, {'type': 'album', 'id': '2QJmrSgbdM35R67eoGQo4j', 'name': '1989', 'shareUrl': 'https://open.spotify.com/album/2QJmrSgbdM35R67eoGQo4j', 'date': '2014-10-27T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e029abdf14e6058bd3903686148', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d000048519abdf14e6058bd3903686148', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b2739abdf14e6058bd3903686148', 'width': 640, 'height': 640}], 'trackCount': 13}, {'type': 'album', 'id': '1KlU96Hw9nlvqpBPlSqcTV', 'name': 'Red (Deluxe Edition)', 'shareUrl': 'https://open.spotify.com/album/1KlU96Hw9nlvqpBPlSqcTV', 'date': '2012-10-22T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e02a7613d346501b828b56a0bc3', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d00004851a7613d346501b828b56a0bc3', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b273a7613d346501b828b56a0bc3', 'width': 640, 'height': 640}], 'trackCount': 22}, {'type': 'album', 'id': '1EoDsNmgTLtmwe1BDAVxV5', 'name': 'Red', 'shareUrl': 'https://open.spotify.com/album/1EoDsNmgTLtmwe1BDAVxV5', 'date': '2012-10-22T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e0296384c98ac4f3e7c2440f5b5', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d0000485196384c98ac4f3e7c2440f5b5', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b27396384c98ac4f3e7c2440f5b5', 'width': 640, 'height': 640}], 'trackCount': 16}, {'type': 'album', 'id': '6fyR4wBPwLHKcRtxgd4sGh', 'name': 'Speak Now World Tour Live', 'shareUrl': 'https://open.spotify.com/album/6fyR4wBPwLHKcRtxgd4sGh', 'date': '2010-10-25T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e02be4ec62353ee75fa11f6d6f7', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d00004851be4ec62353ee75fa11f6d6f7', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b273be4ec62353ee75fa11f6d6f7', 'width': 640, 'height': 640}], 'trackCount': 16}, {'type': 'album', 'id': '5EpMjweRD573ASl7uNiHym', 'name': 'Speak Now (Deluxe Edition)', 'shareUrl': 'https://open.spotify.com/album/5EpMjweRD573ASl7uNiHym', 'date': '2010-10-25T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e022e4ec3175d848eca7b76b07f', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d000048512e4ec3175d848eca7b76b07f', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b2732e4ec3175d848eca7b76b07f', 'width': 640, 'height': 640}], 'trackCount': 20}, {'type': 'album', 'id': '5MfAxS5zz8MlfROjGQVXhy', 'name': 'Speak Now', 'shareUrl': 'https://open.spotify.com/album/5MfAxS5zz8MlfROjGQVXhy', 'date': '2010-10-25T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e02e11a75a2f2ff39cec788a015', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d00004851e11a75a2f2ff39cec788a015', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b273e11a75a2f2ff39cec788a015', 'width': 640, 'height': 640}], 'trackCount': 14}, {'type': 'album', 'id': '43OpbkiiIxJO8ktIB777Nn', 'name': 'Fearless Platinum Edition', 'shareUrl': 'https://open.spotify.com/album/43OpbkiiIxJO8ktIB777Nn', 'date': '2008-11-11T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e0234e5885465afc8a497ac1b7e', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d0000485134e5885465afc8a497ac1b7e', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b27334e5885465afc8a497ac1b7e', 'width': 640, 'height': 640}], 'trackCount': 19}, {'type': 'album', 'id': '2dqn5yOQWdyGwOpOIi9O4x', 'name': 'Fearless', 'shareUrl': 'https://open.spotify.com/album/2dqn5yOQWdyGwOpOIi9O4x', 'date': '2008-11-11T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e027b25c072237f29ee50025fdc', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d000048517b25c072237f29ee50025fdc', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b2737b25c072237f29ee50025fdc', 'width': 640, 'height': 640}], 'trackCount': 13}, {'type': 'album', 'id': '1ycoesYxIFymXWebfmz828', 'name': 'Live From Clear Channel Stripped 2008', 'shareUrl': 'https://open.spotify.com/album/1ycoesYxIFymXWebfmz828', 'date': '2008-06-28T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e02c031e8322b3e8684536ed6d0', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d00004851c031e8322b3e8684536ed6d0', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b273c031e8322b3e8684536ed6d0', 'width': 640, 'height': 640}], 'trackCount': 8}, {'type': 'album', 'id': '7mzrIsaAjnXihW3InKjlC3', 'name': 'Taylor Swift', 'shareUrl': 'https://open.spotify.com/album/7mzrIsaAjnXihW3InKjlC3', 'date': '2006-10-24T00:00:00Z', 'cover': [{'url': 'https://i.scdn.co/image/ab67616d00001e022f8c0fd72a80a93f8c53b96c', 'width': 300, 'height': 300}, {'url': 'https://i.scdn.co/image/ab67616d000048512f8c0fd72a80a93f8c53b96c', 'width': 64, 'height': 64}, {'url': 'https://i.scdn.co/image/ab67616d0000b2732f8c0fd72a80a93f8c53b96c', 'width': 640, 'height': 640}], 'trackCount': 15}]}})




        """ 
        """

    

    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')
    api.add_resource(_Authentication, '/access')
    api.add_resource(_Login, '/login')
    api.add_resource(_Info, '/info')
    api.add_resource(_Output, '/output')
    
