""" /app/auth/views.py"""
from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User

class RegistrationView(MethodView):
    """Handles registration of users"""
    def register(self):
        """Handles POST request to the URL /auth/register"""
        # Query to see if a user already exists
        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            # No user, so register 
            try:
                post_data = request.data
                # Register user
                email = post_data['email']
                password = post_data['password']
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

register_view = RegistrationView.as_view('register_view')
# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func= register_view,
    methods=['POST']
)