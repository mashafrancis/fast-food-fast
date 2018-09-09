import json
import os
import sys
import unittest

from app.models import User

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class UserLoginTest(BaseTests):
    """Tests functionality of user endpoints."""
    def test_login(self):
        """Test API can login a user."""
        response = self.client().post('/v1/auth/register', data=self.user_reg,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('test@gmail.com', str(response.data))
        result = self.client().post('/v1/auth/login', data=self.user_logs,
                                    content_type='application/json')
        self.assertEqual(result.status_code, 200)
        results = json.loads(result.data.decode())
        self.assertTrue(results['access_token'])

    def test_no_login_input(self):
        """Test API login information must be provided."""
        data = json.dumps({'email': '', 'password': ''})
        response = self.client().post('/v1/auth/register', data=self.user_reg,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('test@gmail.com', str(response.data))
        result = self.client().post('/v1/auth/login', data=data,
                                    content_type='application/json')
        self.assertEqual(result.status_code, 400)
        results = json.loads(result.data.decode())
        self.assertEqual(
            results['message'], u"Your email or password is missing!")

