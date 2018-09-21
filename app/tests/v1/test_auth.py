import json
import unittest

from app.api.v1.models.user import User
from .base_test import BaseTests


class AuthTest(BaseTests):
    """Tests functionality of user endpoints."""

    def test_user_registration_and_login(self):
        """Test successful user registration and login."""
        with self.client():
            response = self.register_user('test@gmail.com', 'test1234', 'test1234')
            data = json.loads(response.data.decode())
            self.assertIn('test@gmail.com', str(response.data))
            self.assertIsNotNone(User.find_by_email('test@gmail.com'))
            self.assertIsNotNone(User.find_by_id(1))
            self.assertTrue(data['status'] == 'User Created')
            self.assertTrue(data['message'] == u"User test@gmail.com successfully registered")
            self.assertFalse(data['message'] == u"User successfully registered")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            self.assertNotEqual(response.status_code, 200)

            # Test duplicate registration
            response2 = self.register_user('test@gmail.com', 'test1234', 'test1234')
            data2 = json.loads(response2.data.decode())
            self.assertTrue(data2['status'] == 'Conflict')
            self.assertTrue(data2['message'] == 'User already exists! Please login.')
            self.assertEqual(response2.status_code, 409)

            # Test user login
            response3 = self.login_user('test@gmail.com', 'test1234')
            data3 = json.loads(response3.data.decode())
            self.assertTrue(data3['status'] == 'OK')
            self.assertTrue(data3['message'] == 'You have logged in successfully!')
            self.assertTrue(data3['access_token'])
            self.assertTrue(response3.content_type == 'application/json')
            self.assertEqual(response3.status_code, 200)

            # Test login password is valid
            response4 = self.login_user('test@gmail.com', 'test')
            data4 = json.loads(response4.data.decode())
            self.assertEqual(response4.status_code, 400)
            self.assertTrue(data4['status'] == 'Bad Request')
            self.assertTrue(data4['message'] == 'Wrong Password!')

            # Test user profile
            response5 = self.client().get(
                '/api/v1/auth/profile',
                headers=dict(Authorizarion='Bearer ' + json.loads(
                    response3.data.decode())['access_token']))
            data5 = json.loads(response5.data.decode())
            self.assertTrue(data5['status'] == 'OK')
            # self.assertTrue(data['message'] is not None)
            self.assertEqual(response5.status_code, 200)

            # Test user logout
            self.assertTrue(data['access_token'])
            response6 = self.user_logout(data['access_token'])
            data6 = json.loads(response6.data.decode())
            self.assertEqual(response6.status_code, 200)
            self.assertTrue(data6['status'] == 'Ok')
            self.assertTrue(data6['message'] == 'You have been logged out successfully!')

    def test_user_registration_missing_email(self):
        """Test unsuccessful registration due to missing email"""
        with self.client():
            response = self.register_user('', 'test1234', 'test1234')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Please provide email!')
            self.assertEqual(response.status_code, 400)

    def test_user_registration_missing_password(self):
        """Test unsuccessful registration due to missing password"""
        with self.client():
            response = self.register_user('test@gmail.com', '', 'test1234')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Please provide password!')
            self.assertEqual(response.status_code, 400)

    def test_user_registration_missing_confirmation_password(self):
        """Test unsuccessful registration due to missing confirmation password"""
        with self.client():
            response = self.register_user('test@gmail.com', 'test1234', '')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Please confirm password!')
            self.assertEqual(response.status_code, 400)

    def test_user_email_validity(self):
        """Test unsuccessful registration due to invalid email"""
        with self.client():
            response = self.register_user('test', 'test1234', 'test1234')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Your email is invalid! '
                                               'Kindly provide use with the right email address format')
            self.assertEqual(response.status_code, 400)

    def test_user_invalid_password(self):
        """Test unsuccessful registration due to short password"""
        with self.client():
            response = self.register_user('test@gmail.com', 'tes', 'tes')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Password must contain: '
                                               'lowercase letters, at least a digit, and a min-length of 6')
            self.assertEqual(response.status_code, 400)

    def test_user_mismatch_password(self):
        """Test unsuccessful registration due to short password"""
        with self.client():
            response = self.register_user('test@gmail.com', 'test1234', 'test4321')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Your password must match!')
            self.assertEqual(response.status_code, 400)

    def test_login_non_registered(self):
        """Test login for non-registered user"""
        with self.client():
            response = self.login_user('test@gmail.com', 'test1234')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Not Found')
            self.assertTrue(data['message'] == 'User does not exist. Kindly register!')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_login_has_correct_email(self):
        """Test login email has the correct format"""
        with self.client():
            response = self.login_user('test.com', 'test1234')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertTrue(response.content_type == 'application/json')
            self.assertTrue(data['status'] == 'Unauthorized')
            self.assertTrue(data['message'] == 'Your email is invalid! Kindly recheck your email.')

    def test_user_logout(self):
        """Test a user is logged out with a valid token"""
        with self.client():
            data = self.user_register_login()
            self.assertTrue(data['access_token'])
            response = self.user_logout(data['access_token'])
            data2 = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data2['status'] == 'Ok')
            self.assertTrue(data2['message'] == 'You have been logged out successfully!')


