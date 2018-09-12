import json
import os
import sys
import unittest

from app.models import User
from .base_test import BaseTests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class UsersTest(BaseTests):
    """Tests functionality of user endpoints."""

    def test_user_registration_successful(self):
        """Test successful user registration"""
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
            result['message'],
            u"User already exists! Please login.")

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
            result['message'],
            u"Your email is invalid! Kindly provide use with the right email address format")

        response = self.client().post('/v1/auth/register',
                                      data=data2, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'],
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
            result['message'],
            u"Password must contain: lowercase letters, at least a digit, and a min-length of 6")

        response = self.client().post('/v1/auth/register',
                                      data=data2, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'],
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
            result['message'],
            u"Please provide password!")

        response = self.client().post('/v1/auth/register',
                                      data=data2, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'],
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
            response['message'],
            u"No users to display!")


if __name__ == '__main__':
    unittest.main()
