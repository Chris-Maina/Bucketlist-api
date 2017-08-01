# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response


# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    """wraps creation of new flask obj,
     loads it with configs using app.config,
     connects it with DB,
     returns it  """
    from models import Bucketlist
    from models import User   


    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/auth/register/', methods=['POST'])
    def register():
        # Query to see if a user already exists
        user = User.query.filter_by(email=request.data['email']).first()
        if not user:
            # No user, so register
            try:
                # Register user
                email = request.data['email']
                password = request.data['password']
                user = User(email=email, password=password)
                user.save()
                response = {
                    'message': 'You have been registered successfully. Please login'
                }
                # return the response and a status code 201 (created)
                return make_response(jsonify(response)), 201
            except Exception as e:
                # when there is an error, return error as message
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            # There is a user. Return a message user already exists
            response = {
                'message': 'User already exists. Please login.'
            }
            return make_response(jsonify(response)), 202
    
    @app.route('/auth/login/', methods=['POST'])
    def login():
        """Handles user login"""
        # Create a user object using their email
        user = User.query.filter_by(email=request.data['email']).first()
        # check is user object has sth and password is correct
        if user and user.password_is_correct(request.data['password']):
            # generate an access token
            access_token = user.generate_token(user.id)
            # if an access token is generated, success status_code=OK!
            if access_token:
                response = {
                    'message': "You are logged in successfully",
                    'access_token': access_token.decode()
                }
                return make_response(jsonify(response)), 200
        else:
            # User does not exist, status_code=UNAUTHORIZED
            response = {
                'message': "Invalid email or password, Please try agaon"
            }
            return make_response(jsonify(response)), 401

    @app.route('/bucketlist/', methods=['POST', 'GET'])
    def bucketlists():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                bucketlist = Bucketlist(name=name)
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                })
                response.status_code = 201
                return response
        else:
            # GET
            bucketlists_all = Bucketlist.get_all()
            results = []
            for bucketlist in bucketlists_all:
                obj = {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                }
                results.append(obj)

            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/bucketlist/<int:id>', methods=['PUT', 'GET', 'DELETE'])
    def bucket_edit(id, **kwargs):
        """Handles editing and deletion of specific bucket using id"""
        # retrieve a bucketlist using its ID
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            # if empty raise a 404 error
            abort(404)

        if request.method == 'PUT':
            name = str(request.data.get('name', ''))
            bucketlist.name = name
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            response.status_code = 200
            return response

        elif request.method == 'DELETE':
            bucketlist.delete()
            response = jsonify({
                "message": "bucketlist {} deleted successfully".format(bucketlist.id) 
            })
            response.status_code = 200
            return response

        else:
            # GET
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            response.status_code = 200
            return response    
    return app
