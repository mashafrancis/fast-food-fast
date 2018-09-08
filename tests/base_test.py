import json
import unittest

from app import create_app, models


class BaseTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client

        self.order = json.dumps({
            "name": "Burger",
            "quantity": 2,
            "price": 500
        })

        self.order2 = json.dumps({
            "name": "Burger-2",
            "quantity": 2,
            "price": 500
        })

        self.user_reg = json.dumps({
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'Moonpie1#',
            'confirm_password': 'Moonpie1#'
        })

        self.user_logs = {
            'email': 'test@gmail.com',
            'password': 'Moonpie1#'
        }

        self.user_same_email = json.dumps({
            'username': 'blah',
            'email': 'test@gmail.com',
            'password': 'pie1#Moon',
            'confirm_password': 'pie1#Moon'
        })

    def register(self, email, password, confirm_password):
        return self.app.post(
            '/v1/auth/register',
            data=dict(email=email, password=password, confirm_password=confirm_password),
            follow_redirects=True
        )

    def tearDown(self):
        with self.app.app_context():
            models.all_orders = {}
