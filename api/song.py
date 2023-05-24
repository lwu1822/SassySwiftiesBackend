# from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
# from flask_restful import Api, Resource # used for REST API building
# import requests  # used for testing 
# import random

# from model.songs import *

# songs_api = Blueprint('songs_api', __name__,
#                    url_prefix='/api/songs')

# # API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
# api = Api(songs_api)

# class SongsAPI:
#     # not implemented
#     class _Create(Resource):
#         def post(self, song):
#             pass
            
#     # getJokes()
#     class _Read(Resource):
#         def get(self):
#             return jsonify(getSongs())

#     # getJoke(id)
#     class _ReadID(Resource):
#         def get(self, id):
#             return jsonify(getSong(id))

#     # getRandomJoke()
#     class _ReadRandom(Resource):
#         def get(self):
#             return jsonify(getRandomSong())
    
#     # getRandomJoke()
#     class _ReadCount(Resource):
#         def get(self):
#             count = countSongs()
#             countMsg = {'count': count}
#             return jsonify(countMsg)

#     # put method: addJokeHaHa
#     class _UpdateLike(Resource):
#         def put(self, id):
#             addSongLike(id)
#             return jsonify(getSong(id))

#     # put method: addJokeBooHoo
#     class _UpdateDislike(Resource):
#         def put(self, id):
#             addSongDislike(id)
#             return jsonify(getSong(id))

#     # building RESTapi resources/interfaces, these routes are added to Web Server
#     api.add_resource(_Create, '/create/<string:joke>')
#     api.add_resource(_Read, '/')
#     api.add_resource(_ReadID, '/<int:id>')
#     api.add_resource(_ReadRandom, '/random')
#     api.add_resource(_ReadCount, '/count')
#     api.add_resource(_UpdateLike, '/like/<int:id>')
#     api.add_resource(_UpdateDislike, '/dislike/<int:id>')
    
# if __name__ == "__main__": 
#     # server = "http://127.0.0.1:5000" # run local
#     server = 'https://lwu1822.github.io/SassySwiftiesFrontend/' # run from web
#     url = server + "/api/songs"
#     responses = []  # responses list

#     # get count of jokes on server
#     count_response = requests.get(url+"/count")
#     count_json = count_response.json()
#     count = count_json['count']

#     # update likes/dislikes test sequence
#     num = str(random.randint(0, count-1)) # test a random record
#     responses.append(
#         requests.get(url+"/"+num)  # read joke by id
#         ) 
#     responses.append(
#         requests.put(url+"/like/"+num) # add to like count
#         ) 
#     responses.append(
#         requests.put(url+"/dislike/"+num) # add to jeer count
#         ) 

#     # obtain a random joke
#     responses.append(
#         requests.get(url+"/random")  # read a random joke
#         ) 

#     # cycle through responses
#     for response in responses:
#         print(response)
#         try:
#             print(response.json())
#         except:
#             print("unknown error")