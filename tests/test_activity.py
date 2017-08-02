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
        self.activity = {'name': 'Shop in Dubai'}
        # test bucket
        self.bucketlist = {'name': 'Go to Egypt for trip'}
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

    def register_login_get_token(self):
        # register user
        self.client().post('/auth/register/', data=self.user_details)

        # login user
        result = self.client().post('/auth/login/', data=self.user_details)

        # get token
        access_token = json.loads(result.data.decode())['access_token']
        self.access_token = access_token

        # create bucket
        return self.client().post('/bucketlist/',
                                  headers=dict(
                                      Authorization="Bearer " + access_token),
                                  data=self.bucketlist)

    def test_activity_creation(self):
        """ Test API can create an activity using POST """

        res = self.register_login_get_token()
        self.assertEqual(res.status_code, 201)
        # create a activity
        res = self.client().post('/bucketlist/1/activities',
                                 headers=dict(
                                     Authorization="Bearer " + self.access_token),
                                 data=self.activity)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Shop in', str(res.data))

    def test_api_get_all_activities(self):
        """ Test API can get all activities using GET """
        # create a bucket
        res = self.register_login_get_token()
        self.assertEqual(res.status_code, 201)

        # create a activity
        res = self.client().post('/bucketlist/1/activities',
                                 headers=dict(
                                     Authorization="Bearer " + self.access_token),
                                 data=self.activity)
        self.assertEqual(res.status_code, 201)

        # get activities
        res = self.client().get('/bucketlist/1/activities',
                                headers=dict(
                                    Authorization="Bearer " + self.access_token))
        self.assertEqual(res.status_code, 200)

    def test_api_get_activity_by_id(self):
        """ Test API can get activity by ID using GET """
        # create a bucket
        res = self.register_login_get_token()
        self.assertEqual(res.status_code, 201)

        # create a activity
        res = self.client().post('/bucketlist/1/activities',
                                 headers=dict(
                                     Authorization="Bearer " + self.access_token),
                                 data=self.activity)
        self.assertEqual(res.status_code, 201)
        # get activity created
        activity_created = json.loads(res.data.decode())
        # get activity by its ID
        res = self.client().get('/bucketlist/1/activities/{}'.format(activity_created['id']),
                                headers=dict(
            Authorization="Bearer " + self.access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Shop in', str(res.data))

    def test_activity_can_be_edited(self):
        """ Test API can edit activity using PUT """
        # create a bucket
        res = self.register_login_get_token()
        self.assertEqual(res.status_code, 201)

        # create a activity
        res = self.client().post('/bucketlist/1/activities',
                                 headers=dict(
                                     Authorization="Bearer " + self.access_token),
                                 data={'name': 'Sky dive'})
        self.assertEqual(res.status_code, 201)

        # get activity created
        activity_created = json.loads(res.data.decode())

        # edit activity
        res = self.client().put('/bucketlist/1/activities/{}'.format(activity_created['id']),
                                headers=dict(
                                    Authorization="Bearer " + self.access_token),
                                data={'name': 'Sky diving in Egypt'})

        # get edited activity
        results = self.client().get('/bucketlist/1/activities/{}'.format(activity_created['id']),
                                    headers=dict(
                                        Authorization="Bearer " + self.access_token))
        self.assertIn('Sky diving', str(results.data))
