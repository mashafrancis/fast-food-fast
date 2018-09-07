import json
import unittest

from .base_test import BaseTests


class UsersTest(BaseTests):
    """Tests functionality of user endpoints."""

    def test_user_registration_successful(self):
        """Test successful user registration"""
        response = self.client().post('/auth/register', data=self.user_reg)
        self.assertEqual(response.status_code, 201)
        self.assertIn('test@gmail.com', str(response.data))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"User test@gmail.com successfully registered")

    def test_same_email_registration(self):
        """Test duplicate email registration"""
        response = self.client().post('/auth/register', data=self.user_reg)
        self.assertEqual(response.status_code, 201)
        self.assertIn('test@gmail.com', str(response.data))
        response = self.client().post('/auth/register',
                                      data={
                                          'username': 'blah',
                                          'email': 'test@gmail.com',
                                          'password': 'pie1#Moon',
                                          'repeat_password': 'pie1#Moon'
                                      })
        self.assertEqual(response.status_code, 409)

    def test_register_username_unique(self):
        """Test a unique username"""
        response = self.client().post('/auth/register', data=self.user_reg)
        self.assertEqual(response.status_code, 201)
        self.assertIn('test@gmail.com', str(response.data))
        response = self.client().post('/auth/register',
                                      data={
                                          'username': 'test',
                                          'email': 'blah@gmail.com',
                                          'password': 'pie1#Moon',
                                          'repeat_password': 'pie1#Moon'
                                      })
        self.assertEqual(response.status_code, 409)

    def test_register_invalid_email(self):
        """Test unsuccessful registration due to invalid email"""
        response = self.client().post('/auth/register',
                                      data={
                                          'username': 'test',
                                          'email': 'test',
                                          'password': 'Moonpie1#',
                                          'repeat_password': 'Moonpie1#'
                                      })
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'],
            u"Your email is invalid! Kindly provide use with the right email address format")

        response = self.client().post('/auth/register',
                                      data={
                                          'username': 'test',
                                          'email': '',
                                          'password': 'Moonpie1#',
                                          'repeat_password': 'Moonpie1#'
                                      })
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'],
            u"Kindly provide use with your email!")

    def test_register_invalid_username(self):
        """Test unsuccessful registration due to invalid username"""
        response = self.client().post('/auth/register',
                                      data={
                                          'username': '11',
                                          'email': 'test@gmail.com',
                                          'password': 'Moonpie1#',
                                          'repeat_password': 'Moonpie1#'
                                      })
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'],
            u"Username must contain at least 1 letter and other characters with a minimum length of 4")

        response = self.client().post('/auth/register',
                                      data={
                                          'username': '',
                                          'email': 'test@gmail.com',
                                          'password': 'Moonpie1#',
                                          'repeat_password': 'Moonpie1#'
                                      })
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'],
            u"Please provide a username!")

    def test_register_invalid_password(self):
        """Test unsuccessful registration due to invalid password"""
        response = self.client().post('/auth/register',
                                      data={
                                          'username': 'test',
                                          'email': 'test@gmail.com',
                                          'password': 'foo',
                                          'repeat_password': 'foo'
                                      })
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'],
            u"Password must contain: lowercase letters, at least a digit, and a min-length of 6")

        response = self.client().post('/auth/register',
                                      data={
                                          'username': 'test',
                                          'email': 'test@gmail.com',
                                          'password': '',
                                          'repeat_password': ''
                                      })
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'],
            u"Please provide a password!")

    def test_register_confirmation_password(self):
        """Test unsuccessful registration due to empty confirmation password"""
        response = self.client().post('/auth/register',
                                      data={
                                          'username': 'test',
                                          'email': 'test@gmail.com',
                                          'password': 'moonpie1#',
                                          'repeat_password': ''
                                      })
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'],
            u"Kindly confirm your password!")

        response = self.client().post('/auth/register',
                                      data={
                                          'username': 'test',
                                          'email': 'test@gmail.com',
                                          'password': 'moonpie1#',
                                          'repeat_password': 'moonpie1'
                                      })
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'],
            u"Your password must match!")


if __name__ == '__main__':
    unittest.main()
