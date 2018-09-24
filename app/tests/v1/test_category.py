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


if __name__ == '__main__':
    unittest.main()
