import json
import os
import sys
import unittest

from .base_test import BaseTests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class UserLoginTest(BaseTests):
    """Tests functionality of user endpoints."""

    def test_login(self):
        """Test API can login a user."""
        response = self.client().post('/v1/auth/register', data=self.user_reg,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('test@gmail.com', str(response.data))
        login_response = self.client().post('/v1/auth/login', data=self.user_logs,
                                            content_type='application/json')

        result = json.loads(login_response.data.decode())
        self.assertEqual(result['message'], u"You have logged in successfully.")
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_no_login_input(self):
        """Test API login information must be provided."""
        data = json.dumps({'email': '', 'password': ''})
        response = self.client().post('/v1/auth/login', data=self.user_reg,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('test@gmail.com', str(response.data))
        result = self.client().post('/v1/auth/login', data=data,
                                    content_type='application/json')
        self.assertEqual(result.status_code, 401)
        results = json.loads(result.data.decode())
        self.assertEqual(
            results['message'], u"Your email or password is missing!")

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        non_user = json.dumps({'email': 'blah@gmail.com', 'password': 'notauseryet'})
        response = self.client().post('/v1/auth/login', data=non_user,
                                      content_type='application/json')
        results = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            results['message'], u"Invalid email or password. Please try again!")


if __name__ == '__main__':
    unittest.main()
