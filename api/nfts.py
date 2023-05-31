from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource  # used for REST API building

from model.users import Nfts
from model.users import User

from datetime import datetime

# Blueprint used to create an application instance
nfts_api = Blueprint('nfts_api', __name__,
                             url_prefix='/api/nfts')

# Initializing Flask-RESTful API
# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(nfts_api)


# Class for creating, reading, deleting, and updating nft
class NftAPI(Resource):

    # Create nft
    class _Create(Resource):
        def post(self):
            ''' Read data from json body '''
            body = request.get_json()

            # validate user
            userID = body.get('userID')
            if userID is None:
                return {'message': f'userID is missing'}, 400

            ''' Get user from id given'''
            user = User.query.filter_by(id=userID).first()
            if user is None:
                return {'message': f'Id {id} does not represent a user'}, 400



            # image = user.get('profile')
            uo = Nfts(
                userID=userID,
                nfts=[True, False, False, False, False, False],
                profile=0
            )

            ''' Create nft in database '''

            # create nft in database
            nft = uo.create()
            # success returns json of nft
            if nft:
                return jsonify(nft.read())
            # failure returns error
            return {'message': f'Processed request, format error'}, 210

    # Read nft
    class _Read(Resource):
        def get(self):
            nfts = Nfts.query.all()  # read/extract all nfts from database
            json_ready = [nft.read() for nft in nfts]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # Update nft
    class _Update(Resource):
        def put(self):
            id = request.args.get('id')
            if id is None:
                return {'message': f'id {id} is missing'}, 400

            user = User.query.filter_by(id=id).first()
            if user is None:
                return {'message': f'user not found'}, 404
            
            nft = Nfts.query.filter_by(id=id).first()
            print(nft)
            if nft is None:
                return {'message': f'nft not found'}, 404

            """Update nft associated with the given id"""
            
            nft_money_requirements = [0, 5, 10, 30, 100, 500]
            nfts = [True]
            user_money = user.currentTokens
            index = 1

            while index <= 5:
                if user_money >= nft_money_requirements[index]:
                    nfts.append(True)
                else:
                    nfts.append(False)
                index = index + 1
            print(nfts)
            nft.update(nfts)
            return {'message': f'Updated'}, 200


# Building REST api endpoints
api.add_resource(NftAPI._Create, '/create')  # Create nft
api.add_resource(NftAPI._Read, '/')  # Read nft
api.add_resource(NftAPI._Update, '/update')  # Update nft
