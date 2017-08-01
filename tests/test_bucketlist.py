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

    def register_user(self):
        """Registers a user"""
        return self.client().post('/auth/register/', data=self.user_details)

    def login_user(self):
        """Registers a user"""
        return self.client().post('/auth/login/', data=self.user_details)

    def test_bucketlist_creation(self):
        """ Test API can creat a bucket using POST """
        # Register,login user and get access token
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        #create a bucket
        res = self.client().post('/bucketlist/',
            headers=dict(Authorization="Bearer "+access_token),
            data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go to Borabora', str(res.data))
    
    def test_api_can_get_all_buckets(self):
        """Test API can get buckets using GET"""
        res = self.client().post('/bucketlist/', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/bucketlist/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to Borabora', str(res.data))

    def test_bucket_can_be_edited(self):
        """Test API can edit an existing bucket using PUT"""
        res = self.client().post('/bucketlist/', data={'name':'Eat,pray and code'})
        self.assertEqual(res.status_code, 201)
        res = self.client().put('/bucketlist/1', data={'name':'Dont just eat, but also pray and code'})
        self.assertEqual(res.status_code, 200)
        results = self.client().get('/bucketlist/1')
        self.assertIn('Dont just eat', str(results.data))

    def test_bucketlist_deletion(self):
        """Test API can delete an existing bucket using DELETE request"""
        res = self.client().post('/bucketlist/', data={'name':'Eat,pray and code'})
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/bucketlist/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists after deletion
        results = self.client().get('/bucketlist/1')
        self.assertEqual(results.status_code, 404)

    def tearDown(self):
        """teardown all variables"""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
