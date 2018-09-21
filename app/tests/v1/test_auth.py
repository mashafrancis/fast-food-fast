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

            # Test missing password
            response5 = self.login_user('test@gmail.com', '')
            data5 = json.loads(response5.data.decode())
            self.assertEqual(response5.status_code, 400)
            self.assertTrue(response5.content_type == 'application/json')
            self.assertTrue(data5['status'] == 'Bad Request')
            self.assertTrue(data5['message'] == 'Your password is missing!')

            # Test missing email
            response6 = self.login_user('', 'test1234')
            data6 = json.loads(response6.data.decode())
            self.assertEqual(response6.status_code, 400)
            self.assertTrue(response6.content_type == 'application/json')
            self.assertTrue(data6['status'] == 'Bad Request')
            self.assertTrue(data6['message'] == 'Your email is missing!')

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


if __name__ == '__main__':
    unittest.main()
