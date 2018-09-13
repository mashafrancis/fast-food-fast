import json
import unittest

from app import create_app, models


class BaseTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
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

    def tearDown(self):
        with self.app.app_context():
            models.all_orders = {}
