from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

from model.users import User
from model.users import Scoreboard

from datetime import datetime

scoreboard_api = Blueprint('scoreboard_api', __name__, url_prefix='/api/scores')
api = Api(scoreboard_api)

class FdScoreAPI(Resource):
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            username = body.get('username')
            if username is None or len(username) < 2 or len(username) > 50:
                return {'message': f'Username is missing, is less than 2 characters, or is more than 50 characters'}, 400
            score = body.get('score')
            if score is None:
                return {'message': f'Score is missing'}, 400

            uo = Scoreboard(username=username, score=score)
            score_entry = uo.create()
            if score_entry:
                return jsonify(score_entry.read())
            return {'message': f'Processed {username}, format error'}, 210

    class _Read(Resource):
        def get(self):
            scores = Scoreboard.query.all()
            json_ready = [score.read() for score in scores]
            return jsonify(json_ready)

    
api.add_resource(FdScoreAPI._Create, '/post')
api.add_resource(FdScoreAPI._Read, '/')
