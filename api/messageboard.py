# from flask import Blueprint, request, jsonify
# from flask_restful import Api, Resource # used for REST API building

# from model.users import Post

# # Blueprint used to create an application instance
# messageboard_api = Blueprint('messageboard_api', __name__,
#                    url_prefix='/api/fd')

# # Initializing Flask-RESTful API
# # API docs https://flask-restful.readthedocs.io/en/latest/api.html
# api = Api(messageboard_api)

# # Class for creating, reading, deleting, and updating post
# class FdPostAPI(Resource):        
    
#     # Create post
#     class _Create(Resource):
#         def post(self):
#             ''' Read data from json body '''
#             body = request.get_json()
            
#             ''' Validate input data '''
#             # validate name
#             title = body.get('title')
#             if title is None or len(title) < 2 or len(title) > 30:
#                 return {'message': f'Name is missing, or is less than 2 characters, or is more than 30 characters'}, 210
#             # validate uid
#             text = body.get('text')
#             if text is None or len(text) < 2 or len(text) > 800:
#                 return {'message': f'Text is missing, or is less than 2 characters, or is more than 800 characters'}, 210
#             # validate imageURL
#             imageURL = body.get('imageURL')
#             if imageURL is None:
#                 return {'message': f'imageURL is missing'}, 210
           
#             ''' Create FdPost instance '''
#             uo = Post(title=title, text=text, imageURL=imageURL)
            
#             ''' Additional input error checking '''

            
#             ''' Create post in database '''
#             # create post in database
#             post = uo.create()
#             # success returns json of post
#             if post:
#                 return jsonify(post.read())
#             # failure returns error
#             return {'message': f'Processed {title}, format error'}, 210

#     # Read post
#     class _Read(Resource):
#         def get(self):
#             posts = Post.query.all()    # read/extract all posts from database
#             json_ready = [post.read() for post in posts]  # prepare output in json
#             return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps


#     # Delete post
#     class _Delete(Resource):
#         def delete(self):
#             id = request.args.get('id')
#             if id is None:
#                 return {'message': f'id {id} is missing'}, 400
        
#             post = Post.query.filter_by(id=id).first()
#             if post is None:
#                 return {'message': f'post not found'}, 404

#             post.delete()
#             return {'message': f'Deleted'}, 200
        
#     # Update post
#     class _Update(Resource):
#         def put(self):
#             id = request.args.get('id')
#             if id is None:
#                 return {'message': f'id {id} is missing'}, 400
        
#             post = Post.query.filter_by(id=id).first()
#             if post is None:
#                 return {'message': f'post not found'}, 404
            
#             body = request.get_json()
#             imageURL = body.get('imageURL')
#             if imageURL is None:
#                 return {'message': f'no like change (imageURL) request found'}, 404

#             post.update(imageURL)
#             return {'message': f'Updated'}, 200
        
#     # Building REST api endpoints
#     api.add_resource(_Create, '/post') # Create post
#     api.add_resource(_Read, '/') # Read post
#     api.add_resource(_Delete, '/delete') # Delete post
#     api.add_resource(_Update, '/update') # Update post