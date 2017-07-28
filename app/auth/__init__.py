""" auth/__init__.py"""

from flask import Blueprint

# Create an instance of authentiation blueprint
auth_blueprint = Blueprint('auth', __name__)

from . import views