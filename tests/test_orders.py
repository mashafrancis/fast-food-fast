import json
import unittest
import app
from app import models


class OrderTests(unittest.TestCase):
    """Tests functionality of the orders endpoint"""

    def setUp(self):
        self.app = app.create_app('testing')
        self.client = self.app.test_client()

        self.order = json.dumps({
            "name": "Burger",
            "quantity": "2",
            "price": "500",
            "status": "pending"
        })

    def test_create_order(self):
        """Test API can create an order (POST)"""
        response = self.client().post('/v1/orders', data=self.order)
        self.assertEqual(response.status_code, 201)
        self.assertIn(
            json.dumps({
                "name": "Burger",
                "quantity": "2",
                "price": "500",
                "status": "pending"
            }), str(response.data))

    def test_get_all_orders(self):
        """Tests API can get all orders (GET)"""
        response = self.app.get('/v1/orders')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        with self.app.app_context():
            models.ORDERS = {}


if __name__ == '__main__':
    unittest.main()
