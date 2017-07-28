""" /tests/test_auth.py"""
import unittest
import json
from app import create_app, db

class AuthenticationTestCase(unittest.TestCase):
    """Test case for authentication blueprint"""

    def setUp(self):
        """Set up test env, test client and user"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        # test user
        self.user_details = {
            'email': 'mainachris@gmail.com',
            'password': 'password123'
        }

        with self.app.app_context():
            # create tables
            db.session.close()
            db.drop_all()
            db.create_all()

        def test_registration(self):
            """ Test if registration works"""
            res = self.client().post('/auth/register', data=self.user_details)
            # get json format for the returned results
            result = json.loads(res.data.decode())
            # assert success message and a 201 status code
            self.assertEqual(result['message'], "You have been registered successfully. Please login")
            self.assertEqual(res.status_code, 201)

