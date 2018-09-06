import json
import unittest

from app import models, create_app


class OrderTests(unittest.TestCase):
    """Tests functionality of the orders endpoint"""

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

    def test_create_order(self):
        """Test API can create an order (POST)"""
        response = self.client().post('/v1/orders', data=self.order,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Burger', str(response.data))

    def test_get_all_orders(self):
        """Tests API can get all orders (GET)"""
        response = self.client().post('/v1/orders', data=self.order,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/v1/orders')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Burger', str(response.data))

    def test_get_order_by_id(self):
        """Tests API can get one order by using its id"""
        response = self.client().post('/v1/orders', data=self.order,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/v1/orders/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Burger', str(response.data))

    def test_order_can_be_edited(self):
        """Test API can edit an existing order (PUT)"""
        response = self.client().post('/v1/orders', data=self.order,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client().put('/v1/orders/1', data=self.order2,
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
        results = self.client().get('/v1/orders/1')
        self.assertIn('Burger-2', str(results.data))

    def test_update_non_existing_order(self):
        """Test updating an order that does not exist"""
        response = self.client().put('/v1/orders/100', data=self.order2,
                                     content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_order_deletion(self):
        """Test API can delete and existing order (DELETE)"""
        response = self.client().post('/v1/orders', data=self.order,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client().delete('/v1/orders/1')
        self.assertEqual(response.status_code, 200)

    def test_delete_non_existing(self):
        """Test deleting an order that does not exist"""
        response = self.client().delete('/v1/orders/100')
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            models.all_orders = {}


if __name__ == '__main__':
    unittest.main()
