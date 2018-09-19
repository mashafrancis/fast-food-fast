import unittest

from app.data import Database
from app.api.v1.models import User

from .base_test import BaseTests


class TestUserModel(BaseTests):

    def test_password_setter(self):
        u = User('test@gmail.com', 'test1234', (Database.user_count() + 1), self.is_admin)
        self.assertTrue(u.password is not None)

    def test_password_verification(self):
        u = User('test@gmail.com', 'test1234', (Database.user_count() + 1), self.is_admin)
        self.assertTrue(u.hash_password('test1234'))

    def test_password_salts_are_random(self):
        u1 = User('test1@gmail.com', 'test1234', (Database.user_count() + 1), self.is_admin)
        u2 = User('test2@gmail.com', 'test1234', (Database.user_count() + 1), self.is_admin)
        pass1 = u1.hash_password(u1.password)
        pass2 = u2.hash_password(u2.password)
        self.assertTrue(pass1 != pass2)


if __name__ == '__main__':
    unittest.main()
