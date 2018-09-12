from werkzeug.security import generate_password_hash

from app.users.user import User
from .base_test import BaseTests


class TestUserModel(BaseTests):
    def test_create_user(self):
        user = User('test@gmail.com', 'test1234')

        self.assertEqual(user.email, 'test@gmail.com')
        self.assertEqual(user.password, generate_password_hash('test1234'))

    def test_user_json(self):
        user = User('test@gmail.com', 'test1234')
        expected = {
            'email': 'test@gmail.com',
            'password': 'test1234'
        }
        self.assertEqual(user.to_dict(), expected,
                         "The JSON export of the item is incorrect. /"
                         "Received {}, expected {}".format(user.to_dict(), expected))
