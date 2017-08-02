# app/__init__.py

from functools import wraps
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
    from models import Bucketlist, User, BucketActivities

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    def auth_required(f):
        """Authenticate users. Handles token"""
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Get access token from the header
            auth_header = request.headers.get('Authorization')
            access_token = auth_header.split(" ")[1]
            if access_token:
                # Decode the token and get user id
                user_id = User.decode_token(access_token)
                if not isinstance(user_id, str):
                    return f(user_id=user_id, *args, **kwargs)
                else:
                    # user id is a string(error)
                    message = user_id
                    response = {
                        'message': message
                    }
                    return make_response(jsonify(response)), 401
        return wrapper

    @app.route('/auth/register/', methods=['POST'])
    def register():
        """Handles registration of users"""
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
                'message': "Invalid email or password, Please try again"
            }
            return make_response(jsonify(response)), 401

    @app.route('/bucketlist/', methods=['POST', 'GET'])
    @auth_required
    def bucketlists(user_id):
        """Handles bucket creation"""
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                bucketlist = Bucketlist(name=name, created_by=user_id)
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified,
                    'created_by': user_id
                })

                return make_response(response), 201
        else:
            # Get all buckets created by user
            buckets = Bucketlist.query.filter_by(created_by=user_id)
            results = []
            for item in buckets:
                obj = {
                    'id': item.id,
                    'name': item.name,
                    'date_created': item.date_created,
                    'date_modified': item.date_modified,
                    'created_by': item.created_by
                }
                results.append(obj)

            return make_response(jsonify(results)), 200

    @app.route('/bucketlist/<int:id>', methods=['PUT', 'GET', 'DELETE'])
    @auth_required
    def bucket_edit(id, **kwargs):
        """Handles editing and deletion of specific bucket using id"""
        # retrieve a bucket using its ID
        bucket = Bucketlist.query.filter_by(id=id).first()
        if not bucket:
            # if empty raise a 404 error. No bucket with this ID
            abort(404)

        if request.method == 'PUT':
            # obtain new name form request
            name = str(request.data.get('name', ''))
            bucket.name = name
            bucket.save()
            response = jsonify({
                'id': bucket.id,
                'name': bucket.name,
                'date_created': bucket.date_created,
                'date_modified': bucket.date_modified,
                'created_by': bucket.created_by
            })
            return make_response(response), 200

        elif request.method == 'DELETE':
            bucket.delete()
            return {
                'message': "bucket {} deleted".format(bucket['id'])
            }, 200

        else:
            # handle GET
            response = jsonify({
                'id': bucket.id,
                'name': bucket.name,
                'date_created': bucket.date_created,
                'date_modified': bucket.date_modified,
                'created_by': bucket.created_by
            })
            return make_response(response), 200

    @app.route('/bucketlist/<int:id>/activities', methods=['POST', 'GET'])
    @auth_required
    def activity(id, user_id):
        """Handles creation of activities"""
        if request.method == 'POST':
            name = str(request.data.get('name', ''))
            if name:
                # there is a name
                bucketactivities = BucketActivities(name,id,user_id)
                bucketactivities.save()
                response = jsonify({
                    'id': bucketactivities.id,
                    'name': bucketactivities.name,
                    'date_created': bucketactivities.date_created,
                    'date_modified': bucketactivities.date_modified,
                    'bucket_id': bucketactivities.bucket,
                    'created_by': user_id
                })
                return make_response(response), 201
        else:
            # Get all activites for a bucket id and user
            activities = BucketActivities.query.filter_by(bucket_id=id,created_by=user_id)
            results = []
            for item in activities:
                obj = {
                    'id': item.id,
                    'name': item.name,
                    'date_created': item.date_created,
                    'date_modified': item.date_modified,
                    'bucket_id': item.bucket,
                    'created_by': item.created_by
                }
                results.append(obj)

            return make_response(jsonify(results)), 200



    return app
