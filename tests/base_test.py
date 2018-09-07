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

        self.user_reg = {
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'Moonpie1#',
            'repeat_password': 'Moonpie1#'
        }

        self.user_logs = {
            'email': 'test@gmail.com',
            'password': 'Moonpie1#'
        }

    def tearDown(self):
        with self.app.app_context():
            models.all_orders = {}
