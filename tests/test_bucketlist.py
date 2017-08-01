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
        self.bucketlist = {'name': 'Go to Borabora for trip'}
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

        # create a bucket
        res = self.client().post('/bucketlist/',
                                 headers=dict(
                                     Authorization="Bearer " + access_token),
                                 data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_all_buckets(self):
        """Test API can get buckets using GET"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # create a bucket
        res = self.client().post('/bucketlist/',
                                 headers=dict(
                                     Authorization="Bearer " + access_token),
                                 data=self.bucketlist)
        self.assertEqual(res.status_code, 201)

        # get buckets belonging to user
        res = self.client().get('/bucketlist/',
                                headers=dict(
                                    Authorization="Bearer " + access_token),
                                )
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to Borabora', str(res.data))

    def test_bucket_can_be_edited(self):
        """Test API can edit an existing bucket using PUT"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # create a bucket
        res = self.client().post('/bucketlist/',
                                 headers=dict(
                                     Authorization="Bearer " + access_token),
                                 data={'name': 'Hiking'})
        self.assertEqual(res.status_code, 201)

        # get the bucket created
        bucket_to_edit = json.loads(res.data.decode())

        # edit the bucket
        res = self.client().put("/bucketlist/{}".format(bucket_to_edit['id']),
                                headers=dict(
                                    Authorization="Bearer " + access_token),
                                data={'name': 'Hike in Ngong hills'})
        self.assertEqual(res.status_code, 200)

        # get the edited bucket
        results = self.client().get("/bucketlist/{}".format(bucket_to_edit['id']),
                                    headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('Hike in', str(results.data))

    def test_bucketlist_deletion(self):
        """Test API can delete an existing bucket using DELETE request"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # create a bucket
        res = self.client().post('/bucketlist/',
                                 headers=dict(
                                     Authorization="Bearer " + access_token),
                                 data={'name': 'Hiking'})
        self.assertEqual(res.status_code, 201)

        # get bucket to delete
        bucket_to_delete = json.loads(res.data.decode())

        # delete bucket created
        res = self.client().delete('/bucketlist/{}'.format(bucket_to_delete['id']),
                                    headers=dict(Authorization="Bearer "+ access_token)
                                    )
        self.assertEqual(res.status_code, 200)

        # Test to see if it exists after deletion
        results = self.client().get('/bucketlist/{}'.format(bucket_to_delete['id']),
                                    headers=dict(Authorization="Bearer "+ access_token)
                                    )
        self.assertEqual(results.status_code, 404)

    def tearDown(self):
        """teardown all variables"""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
