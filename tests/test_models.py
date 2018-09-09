from app.models import User
from .base_test import BaseTests


class TestUserModel(BaseTests):
    def test_create_user(self):
        user = User('test', 'test@gmail.com', 'test1234', 'test1234')

        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertEqual(user.password, 'test1234')
        self.assertEqual(user.confirm_password, 'test1234')

    def test_user_json(self):
        user = User('test', 'test@gmail.com', 'test1234', 'test1234')
        expected = {
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'test1234'
        }
        self.assertEqual(user.json(), expected,
                         "The JSON export of the item is incorrect. /"
                         "Received {}, expected {}".format(user.json(), expected))
