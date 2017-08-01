# test_activity.py
import unittest
import json
from app import create_app, db

class BucketActivitiesTestCase(unittest.TestCase):
    """Class represents the test cases for bucket activities"""
    def setUp(self):
        """
        Initializes app,test variables and test client
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.activities = {'name':'Shop in Dubai'}
        # test user
        self.user_details = {
            'email': 'test@gmail.com',
            'password': 'password123'
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()
