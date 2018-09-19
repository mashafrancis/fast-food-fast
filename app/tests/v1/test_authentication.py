import json
import unittest

from app.models import User
from .base_test import BaseTests


class UsersTest(BaseTests):
    """Tests functionality of user endpoints."""

    def test_user_registration_successful(self):
        """Test successful user registration"""
        data = json.dumps({'email': '', 'password': 'blahbla2'})
        data1 = json.dumps({'email': 'test@gmail.com', 'password': ''})
        data2 = json.dumps({'email': 'test@gmail.com', 'password': 'blah'})

        response = self.client().post('/v1/auth/register', data=self.user_reg,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('test@gmail.com', str(response.data))
        self.assertIsNotNone(User.find_by_email('test@gmail.com'))
        self.assertIsNotNone(User.find_by_id(1))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"User test@gmail.com successfully registered")

        # Test API can get all users.
        self.assertIn('test@gmail.com', str(response.data))
        response = self.client().get('/v1/auth/register')
        self.assertEqual(response.status_code, 200)

        # Test unsuccessful registration due to duplicate email
        response = self.client().post('/v1/auth/register',
                                      data=self.user_same_email, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['error'],
            u"User already exists! Please login.")

        login_response = self.client().post('/v1/auth/login', data=self.user_logs,
                                            content_type='application/json')

        result = json.loads(login_response.data.decode())
        self.assertEqual(result['message'], u"You have logged in successfully.")
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(result['access_token'])

        # Test email missing email
        result = self.client().post('/v1/auth/login', data=data,
                                    content_type='application/json')
        self.assertEqual(result.status_code, 400)
        results = json.loads(result.data.decode())
        self.assertEqual(
            results['error'], u"Your email is missing!")

        # Test missing password
        result = self.client().post('/v1/auth/login', data=data1,
                                    content_type='application/json')
        self.assertEqual(result.status_code, 400)
        results = json.loads(result.data.decode())
        self.assertEqual(
            results['error'], u"Your password is missing!")

        # Test mismatch password
        result = self.client().post('/v1/auth/login', data=data2,
                                    content_type='application/json')
        self.assertEqual(result.status_code, 400)
        results = json.loads(result.data.decode())
        self.assertEqual(
            results['error'], u"Wrong Password!")

    def test_register_invalid_email(self):
        """Test unsuccessful registration due to invalid email"""
        data = json.dumps({
            'email': 'test', 'password': 'Moonpie1#', 'confirm_password': 'Moonpie1#'})
        data2 = json.dumps({
            'email': '', 'password': 'Moonpie1#', 'confirm_password': 'Moonpie1#'})

        response = self.client().post('/v1/auth/register',
                                      data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['error'],
            u"Your email is invalid! Kindly provide use with the right email address format")

        # Test email not provided
        response = self.client().post('/v1/auth/register',
                                      data=data2, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['error'],
            u"Please provide email!")

    def test_register_invalid_password(self):
        """Test unsuccessful registration due to invalid password"""
        data = json.dumps({
            'email': 'test@gmail.com', 'password': 'foo', 'confirm_password': 'foo'})
        data2 = json.dumps({
            'email': 'test@gmail.com', 'password': '', 'confirm_password': ''})
        response = self.client().post('/v1/auth/register',
                                      data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['error'],
            u"Password must contain: lowercase letters, at least a digit, and a min-length of 6")

        # Test password not provided
        response = self.client().post('/v1/auth/register',
                                      data=data2, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['error'],
            u"Please provide password!")

    def test_register_confirmation_password(self):
        """Test unsuccessful registration due to empty confirmation password"""
        data = json.dumps({
            'email': 'test@gmail.com', 'password': 'moonpie1#', 'confirm_password': ''})
        data2 = json.dumps({
            'email': 'test@gmail.com', 'password': 'moonpie1#', 'confirm_password': 'moonpie1'})
        response = self.client().post('/v1/auth/register',
                                      data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['error'],
            u"Please provide password!")

        response = self.client().post('/v1/auth/register',
                                      data=data2, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['error'],
            u"Your password must match!")

    def test_user_whitespace_passwords(self):
        """Tests unsuccessful registration due to whitespace passwords"""
        data = json.dumps({
            'email': 'test@gmail.com', 'password': '       ', 'confirm_password': '       '})
        response = self.client().post('/v1/auth/register',
                                      data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_no_user_found(self):
        """ Test API can return no users found."""
        response = self.client().get('/v1/auth/register')
        self.assertEqual(response.status_code, 404)
        response = json.loads(response.data.decode())
        self.assertEqual(
            response['error'],
            u"No users to display!")

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        non_user = json.dumps({'email': 'blah@gmail.com', 'password': 'notauseryet'})
        response = self.client().post('/v1/auth/login', data=non_user,
                                      content_type='application/json')
        results = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            results['error'], u"User does not exist. Kindly register!")

    def test_no_token_get_all(self):
        """Test unauthorized to get all users without a token."""
        response = self.client().get('/v1/users')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test token is not in use."""
        self.client().post('/v1/auth/register', data=self.user_reg)
        result = self.client().post('/v1/auth/login', data=self.user_logs)
        access_token = json.loads(result.data.decode())['access_token']
        self.client().post('/auth/logout',
                           headers=dict(Authorization="Bearer " + access_token))
        response = self.client().post('/orders',
                                      headers=dict(Authorization="Bearer " + access_token),
                                      data=self.order)
        return response
        results = json.loads(response.data.decode())
        self.assertEqual(results['error'], u"No token provided!")

    def test_header_without_token(self):
        """Test header exists but it has no token."""
        response = self.client().post('/orders',
                                      headers=dict(Authorization="Bearer "),
                                      data=self.order)
        return response
        results = json.loads(response.data.decode())
        self.assertEqual(results['error'], u"No access token!")


if __name__ == '__main__':
    unittest.main()
