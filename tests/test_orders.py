import json
import unittest

from .base_test import BaseTests


class OrderTests(BaseTests):
    """Tests functionality of the orders endpoint"""

    def register_user(self):
        return self.client().post('/v1/auth/register', data=self.user_reg)

    def login_user(self):
        return self.client().post('/v1/auth/login', data=self.user_logs)

    def test_create_order(self):
        """Test API can create an order (POST)"""
        # Register a test user then log in.
        self.register_user()
        result = self.login_user()

        # Obtain access token
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().post('/v1/orders',
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token),
                                      data=self.order)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Burger', str(response.data))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"Order has been added successfully.")

    def test_get_all_orders(self):
        """Tests API can get all orders (GET)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # Test for no orders found.
        response = self.client().get('/v1/orders',
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['error'], u"Sorry, No orders for you!")

        # Test user cannot delete non existent orders
        response = self.client().delete('/v1/orders',
                                        headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['error'], u"No orders available!")

        # Test for orders found.
        response = self.client().post('/v1/orders',
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token),
                                      data=self.order)
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/v1/orders')
        self.assertEqual(response.status_code, 200)

    def test_get_order_by_id(self):
        """Tests API can get one order by using its id"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # Test for no orders found.
        response = self.client().get('/v1/orders/2',
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['error'], u"Sorry, Order No 2 does't exist!")

        # Test get order by order_id
        response = self.client().post('/v1/orders',
                                      headers=dict(Authorization="Bearer " + access_token),
                                      content_type='application/json',
                                      data=self.order,)
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/v1/orders/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Burger', str(response.data))

    def test_order_can_be_edited(self):
        """Test API can edit an existing order (PUT)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # Test for non existing order
        response = self.client().put('/v1/orders/100',
                                     data=self.order2,
                                     content_type='application/json',
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['error'], u"Sorry, Order No 100 doesn't exist yet! Create one.")

        response = self.client().post('/v1/orders',
                                      data=self.order,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)
        response = self.client().put('/v1/orders/1',
                                     data=self.order2,
                                     content_type='application/json',
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 200)
        results = self.client().get('/v1/orders/1')
        self.assertIn('Burger-2', str(results.data))

    def test_update_non_existing_order(self):
        """Test updating an order that does not exist"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().put('/v1/orders/100',
                                     data=self.order2,
                                     content_type='application/json',
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 404)

    def test_delete_all_orders(self):
        """Test API can delete all orders (DELETE)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().post('/v1/orders',
                                      data=self.order,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)
        response = self.client().post('/v1/orders',
                                      data=self.order2,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)
        response = self.client().delete('/v1/orders')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"All orders have been successfully deleted!")

    def test_order_deletion(self):
        """Test API can delete and existing order (DELETE)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # Test deleting non existing order.
        response = self.client().delete('/v1/orders/10',
                                        headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['error'], u"Order No 10 does not exist!")

        response = self.client().post('/v1/orders',
                                      data=self.order,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)
        response = self.client().delete('/v1/orders/1')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u"Order No 1 has been deleted!")


if __name__ == '__main__':
    unittest.main()
