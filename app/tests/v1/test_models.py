import unittest

from app.api.v1.models.user import User
from app.data import Database

from .base_test import BaseTests


class TestUserModel(BaseTests):

    def test_password_setter(self):
        u = User('test@gmail.com', 'test1234')
        self.assertTrue(u.password is not None)

    def test_password_verification(self):
        u = User('test@gmail.com', 'test1234')
        self.assertTrue(u.hash_password('test1234'))

    def test_password_salts_are_random(self):
        u1 = User('test1@gmail.com', 'test1234')
        u2 = User('test2@gmail.com', 'test1234')
        pass1 = u1.hash_password(u1.password)
        pass2 = u2.hash_password(u2.password)
        self.assertTrue(pass1 != pass2)

    def test_encode_access_token(self):
        u = User('test@gmail.com', 'test1234')
        u.add_user()
        access_token = u.generate_token(u.user_id)
        self.assertTrue(isinstance(access_token, bytes))

    def test_decode_access_token(self):
        u = User('test@gmail.com', 'test1234')
        u.add_user()
        access_token = u.generate_token(u.user_id)
        self.assertTrue(isinstance(access_token, bytes))
        self.assertTrue(User.decode_token(access_token) == 1)


if __name__ == '__main__':
    unittest.main()
