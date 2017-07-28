# app/models.py
from app import db
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "hardworkpayseverytime"


class User(db.Model):
    """ Defines users table to help keep track of users"""

    __tablename__ = 'users'

    # Define columns for users table
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    bucketlists = db.relationship(
        'Bucketlist', order_by='Bucketlist.id', cascade="all, delete-orphan")

    def __init__(self, email, password):
        """Initialize user with email and password"""
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_correct(self, password):
        """ Check if hash of passwords are equal hash(self.password)=hash(password)"""
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """ Save user in the db """
        db.session.add(self)
        db.session.commit()
        
    def generate_token(self, user_id):
        """Code to generate and encode a token before its sent to user"""
        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string encoded token using payload and SECRET key
            jwt_string = jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """ Handles the decoding of a token from the Authorization header"""
        try:
            # Decode token with our secret key
            payload = jwt.decode(token, SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # token has expired
            return "Timed out. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"


class Bucketlist(db.Model):
    """This class represents the bucketlist table"""
    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, name, created_by):
        """Initialize bucket with name and user who created it"""
        self.name = name
        self.created_by = created_by

    def save(self):
        """Saves data to db"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        """Gets buckets belonging to user who created them"""
        return Bucketlist.query.filter_by(created_by=user_id)

    def delete(self):
        """Deletes a given bucket"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Returns a representation of a bucketlist instance"""
        return "<Bucketlist: {}>".format(self.name)
