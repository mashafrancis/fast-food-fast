import json
import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class UsersTest(BaseTests):
    """Tests functionality of user endpoints."""

    def test_user_registration_successful(self):
        """Test successful user registration"""
        response = self.client().post('/v1/auth/register', data=self.user_reg,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('test@gmail.com', str(response.data))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"User test@gmail.com successfully registered")

    def test_register_invalid_email(self):
        """Test unsuccessful registration due to invalid email"""
        data = json.dumps({
            'username': 'test', 'email': 'test',
            'password': 'Moonpie1#', 'confirm_password': 'Moonpie1#'})
        data2 = json.dumps({
            'username': 'test', 'email': '',
            'password': 'Moonpie1#', 'confirm_password': 'Moonpie1#'})
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

    def test_register_invalid_username(self):
        """Test unsuccessful registration due to invalid username"""
        data = json.dumps({
            'username': '11', 'email': 'test@gmail.com',
            'password': 'Moonpie1#', 'confirm_password': 'Moonpie1#'})
        data2 = json.dumps({
            'username': '', 'email': 'test@gmail.com',
            'password': 'Moonpie1#', 'confirm_password': 'Moonpie1#'})
        response = self.client().post('/v1/auth/register',
                                      data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'],
            u"Username must contain at least 1 letter and other characters with a minimum length of 4")

        response = self.client().post('/v1/auth/register',
                                      data=data2, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'],
            u"Please provide username!")

    def test_register_invalid_password(self):
        """Test unsuccessful registration due to invalid password"""
        data = json.dumps({
            'username': 'test', 'email': 'test@gmail.com',
            'password': 'foo', 'confirm_password': 'foo'})
        data2 = json.dumps({
            'username': 'test', 'email': 'test@gmail.com',
            'password': '', 'confirm_password': ''})
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
            'username': 'test', 'email': 'test@gmail.com',
            'password': 'moonpie1#', 'confirm_password': ''})
        data2 = json.dumps({
            'username': 'test', 'email': 'test@gmail.com',
            'password': 'moonpie1#', 'confirm_password': 'moonpie1'})
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


if __name__ == '__main__':
    unittest.main()
