""" /tests/test_auth.py"""
import unittest
import json
from app import create_app, db

class AuthenticationTestCase(unittest.TestCase):
    """Test case for authentication blueprint
    Test user registration
    Test user login
    Test user login with non existent email/password
    """

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
        res = self.client().post('/auth/register/', data=self.user_details)
        # get json format for the returned results
        result = json.loads(res.data.decode())
        # assert success message and a 201 status code
        self.assertEqual(result['message'], "You have been registered successfully. Please login")
        self.assertEqual(res.status_code, 201)

    def test_user_login(self):
        """Test user can login after registration"""
        res = self.client().post('/auth/register/', data=self.user_details)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/auth/login/', data=self.user_details)
        # Get the response in json format
        result = json.loads(login_res.data.decode())
        # Test response
        self.assertEqual(result['message'], "You are logged in successfully")
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_login_non_existent_user(self):
        """Tests user login with non existent email&password"""
        user_details = {
            'email': "test@gmail.com",
            'password': "testpassword"
        }
        res = self.client().post('/auth/login/', data=user_details)
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(result['message'], "Invalid email or password, Please try again")
        