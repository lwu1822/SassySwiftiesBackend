from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.users import Post
from model.users import User

from datetime import datetime

# Blueprint used to create an application instance
messageboard_api = Blueprint('messageboard_api', __name__,
                   url_prefix='/api/posts')

# Initializing Flask-RESTful API
# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(messageboard_api)

# Class for creating, reading, deleting, and updating post
class FdPostAPI(Resource):        
    
    # Create post
    class _Create(Resource):
        def post(self):
            ''' Read data from json body '''
            body = request.get_json()
            ''' Validate input data '''
            # validate name
            title = body.get('title')
            if title is None or len(title) < 2 or len(title) > 50:
                return {'message': f'Name is missing, is less than 2 characters, or is more than 50 characters'}, 400
            # validate uid
            text = body.get('text')
            if text is None or len(text) < 2 or len(text) > 500:
                return {'message': f'Text is missing, is less than 2 characters, or is more than 500 characters'}, 400
            
            # validate user
            userID = body.get('userID')
            if userID is None:
                return {'message': f'userID is missing'}, 400
            
           
            ''' Get user from id given'''
            user = User.query.filter_by(id=userID).first()
            if user is None:
                return {'message': f'Id {id} does not represent a user'}, 400
            
            username = user.username
            if username is None:
                return {'message': f'Requested user at id {id} does not have a username'}, 400

            image = user.profile
            if image is None:
                return {'message': f'Requested user at id {id} does not have a profile'}, 400
            # image = user.get('profile')
            
            uo = Post(
                title=title,
                note=text,
                date=datetime.now().strftime('%Y/%m/%d'),
                username=username,
                image=image,
                profile=profile
            )
            
            ''' Create post in database '''

            # create post in database
            post = uo.create()
            # success returns json of post
            if post:
                return jsonify(post.read())
            # failure returns error
            return {'message': f'Processed {title}, format error'}, 210

    # Read post
    class _Read(Resource):
        def get(self):
            posts = Post.query.all()    # read/extract all posts from database
            json_ready = [post.read() for post in posts]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps


    # Delete post
    class _Delete(Resource):
        def delete(self):
            id = request.args.get('id')
            if id is None:
                return {'message': f'id {id} is missing'}, 400
        
            post = Post.query.filter_by(id=id).first()
            if post is None:
                return {'message': f'post not found'}, 404

            post.delete()
            return {'message': f'Deleted'}, 200
        
    # Update post
    class _Update(Resource):
        def put(self):
            id = request.args.get('id')
            if id is None:
                return {'message': f'id {id} is missing'}, 400
        
            post = Post.query.filter_by(id=id).first()
            if post is None:
                return {'message': f'post not found'}, 404
            
            body = request.get_json()
            likes = body.get('likes')
            add = body.get('add')
            remove = body.get('remove')

            if likes is None and add is None and remove is None:
                return {'message': f'no like change request found'}, 404
            
            if likes is not None:
                post.update(likes = likes)
            if add is not None: 
                 post.update(add_like = add)
            if remove is not None: 
                 post.update(remove_like = remove)

            return {'message': f'Updated'}, 200
        
    # Building REST api endpoints
    api.add_resource(_Create, '/post') # Create post
    api.add_resource(_Read, '/') # Read post
    api.add_resource(_Delete, '/delete') # Delete post
    api.add_resource(_Update, '/update') # Update post