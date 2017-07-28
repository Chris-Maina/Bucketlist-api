# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    """wraps creation of new flask obj,
     loads it with configs using app.config,
     connects it with DB,
     returns it  """
    from app.models import Bucketlist


    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

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

    @app.route('/bucketlist/<int:id>', methods=['PUT','GET'])
    def bucket_edit(id, **kwargs):
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
