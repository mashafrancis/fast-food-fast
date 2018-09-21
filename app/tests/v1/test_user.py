import json
import unittest

from .base_test import BaseTests


class UserTest(BaseTests):
    """Tests functionality of user endpoints."""
    def test_get_all_users(self):
        """Tests API can get all users (GET)"""
        access_token = self.user_token_get()

        # Test for users found.
        self.user_register_login()
        response = self.client().get('/api/v1/users',
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 200)

        # Test API can get a single user by ID
        response = self.client().get('/api/v1/users/1')
        self.assertEqual(response.status_code, 200)

        # Test API can get a non existent user
        response = self.client().get('/api/v1/users/10')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['status'] == 'Not Found')
        self.assertEqual(data['message'], u"Sorry, User ID No 10 does't exist!")


if __name__ == '__main__':
    unittest.main()
