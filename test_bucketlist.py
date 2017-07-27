# test_bucketlist.py
import unittest
import os
import json
from app import create_app, db

class BucketlistTestCase(unittest.TestCase):
    """Class represents the test cases for a the bucketlist"""

    def setUp(self):
        """
        Initializes app,test variables and test client
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name':'Go to Borabora for trip'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_bucketlist_creation(self):
        """ Test API can creat a bucket using POST """
        res = self.client().post('/bucketlist/', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go to Borabora', str(res.data))

    def tearDown(self):
        """teardown all variables"""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
