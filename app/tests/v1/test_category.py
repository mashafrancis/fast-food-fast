import json
import unittest

from .base_test import BaseTests


class CategoryTests(BaseTests):
    """Tests functionality of the category endpoint"""

    def test_create_new_category(self):
        """Test API can create an order (POST)"""
        access_token = self.user_token_get()

        response = self.client().post('/api/v1/category', data=self.category,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == u"A new category has been added successfully.")
        self.assertFalse(data['message'] == u"Category has been added successfully.")

    def test_get_all_categories(self):
        """Tests API can get all categories (GET)"""
        access_token = self.user_token_get()

        # Test for no category found.
        response = self.client().get('/api/v1/category',
                                     headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'Not Found')
        self.assertEqual(data['message'], u"Sorry, No Category found! Create one.")
        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 401)

        # Test user cannot delete non existent categories
        response = self.client().delete('/api/v1/category',
                                        headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'Not Found')
        self.assertEqual(data['message'], u"There is no category here!")
        self.assertEqual(response.status_code, 404)

        # Test for categories found.
        response = self.client().post('/api/v1/category', data=self.category,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/api/v1/category',
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 200)

    def test_delete_all_orders(self):
        """Test API can delete all categories (DELETE)"""
        access_token = self.user_token_get()

        response = self.client().post('/api/v1/category', data=self.category,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)

        response = self.client().post('/api/v1/category', data=self.category2,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)

        response = self.client().delete('/api/v1/category',
                                        headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'OK')
        self.assertEqual(data['message'], u"All categories have been successfully deleted!")
        self.assertEqual(response.status_code, 200)

    def test_get_category_by_id(self):
        """Tests API can get one order by using its id"""
        access_token = self.user_token_get()

        # Test for no orders found.
        response = self.client().get('/api/v1/category/2',
                                     headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'Not Found')
        self.assertEqual(data['message'], u"Sorry, Category does't exist!")
        self.assertEqual(response.status_code, 404)

        # Test get order by order_id
        response = self.client().post('/api/v1/category', data=self.category,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/api/v1/category/1',
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Burger', str(response.data))


if __name__ == '__main__':
    unittest.main()
