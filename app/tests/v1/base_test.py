import json
import os
import sys  # Fix import errors
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.api.v1 import models


class BaseTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client

        self.order = json.dumps({
            'name': 'Burger',
            'quantity': '10',
            'price': '1000',
            'created_by': 'Test'
        })

        self.order2 = json.dumps({
            'name': 'Burger-2',
            'quantity': '20',
            'price': '2000',
            'created_by': 'Test',
            'status': 'Accepted'
        })

        self.user_reg = json.dumps({
            'email': 'test@gmail.com',
            'password': 'Moonpie1#',
            'confirm_password': 'Moonpie1#'
        })

        self.user_logs = json.dumps({
            'email': 'test@gmail.com',
            'password': 'Moonpie1#'
        })

        self.user_same_email = json.dumps({
            'email': 'test@gmail.com',
            'password': 'pie1#Moon',
            'confirm_password': 'pie1#Moon'
        })

        self.user_same_username = json.dumps({
            'email': 'blah@gmail.com',
            'password': 'pie1#Moon',
            'confirm_password': 'pie1#Moon'
        })

    def register_user(self, email, password, confirm_password):
        """Register user with dummy data"""
        return self.client().post(
            '/api/v1/auth/register',
            content_type='application/json',
            data=json.dumps(dict(email=email, password=password, confirm_password=confirm_password)))

    def register_user_wrong_content(self, email, password, confirm_password):
        """Register user with dummy data"""
        return self.client().post(
            '/api/v1/auth/register',
            content_type='wrong',
            data=json.dumps(dict(email=email, password=password, confirm_password=confirm_password)))

    def login_user(self, email, password):
        """Register user with dummy data"""
        return self.client().post(
            '/api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(dict(email=email, password=password)))

    def user_register_login(self):
        """Method for registration and login"""
        # Register user
        response = self.register_user('moonpie@gmail.com', 'test1234', 'test1234')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'Created')
        self.assertTrue(data['message'] == u"User test@gmail.com successfully registered")
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.stattus_code, 201)

        # Login user
        response2 = self.login_user('test@gmail.com', 'test1234')
        data2 = json.loads(response2.data.decode())
        self.assertTrue(data2['status'] == 'OK')
        self.assertTrue(data2['message'] == 'You have logged in successfully!')
        self.assertTrue(response2.content_type == 'application/json')
        self.assertEqual(response2.status_code, 200)
        self.assertTrue(data2['access_token'])

        return data2

    def user_logout(self, token):
        """Method to logout a user"""
        response = self.client().post(
            '/api/v1/auth/logout',
            headers=dict(Authorization='Bearer ' + token))
        return response

    def get_user_token(self):
        """Get user token"""
        response = self.register_user('test@gmail.com', 'test1234', 'test1234')
        return json.loads(response.data.decode())['access_token']

    def create_order(self, token):
        """Create a dummy order"""
        response = self.client().post(
            '/api/v1/orders',
            data=self.order,
            headers=dict(Authorization='Bearer ' + token),
            content_type='application/json'
        )
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('Burger', str(response.data))
        self.assertEqual(result['message'], u"Order has been added successfully.")

    def tearDown(self):
        with self.app.app_context():
            models.all_orders = {}
