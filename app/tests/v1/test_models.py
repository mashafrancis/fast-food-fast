import unittest

from app.api.v1.models.user import User

from .base_test import BaseTests


class TestUserModel(BaseTests):

    def test_password_setter(self):
        u = User('tester', 'test@gmail.com', 'test1234')
        self.assertTrue(u.password is not None)

    def test_password_verification(self):
        u = User('tester1', 'test@gmail.com', 'test1234')
        self.assertTrue(u.hash_password('test1234'))

    def test_password_salts_are_random(self):
        u1 = User('tester2', 'test1@gmail.com', 'test1234')
        u2 = User('tester3', 'test2@gmail.com', 'test1234')
        pass1 = u1.hash_password(u1.password)
        pass2 = u2.hash_password(u2.password)
        self.assertTrue(pass1 != pass2)

    def test_encode_access_token(self):
        u = User('tester4', 'test@gmail.com', 'test1234')
        u.add_user()
        access_token = u.generate_token(u.user_id)
        self.assertTrue(isinstance(access_token, bytes))

    def test_user_has_attributes(self):
        self.assertEqual(hasattr(User, 'generate_token'), True)
        self.assertEqual(hasattr(User, 'add_user'), True)
        self.assertEqual(hasattr(User, 'list_all_users'), True)
        self.assertEqual(hasattr(User, 'find_by_email'), True)
        self.assertEqual(hasattr(User, 'find_by_id'), True)
        self.assertEqual(hasattr(User, 'find_by_username'), True)
        self.assertEqual(hasattr(User, 'delete'), True)
        self.assertEqual(hasattr(User, 'hash_password'), True)
        self.assertEqual(hasattr(User, 'check_hashed_password'), True)
        self.assertEqual(hasattr(User, 'decode_token'), True)


if __name__ == '__main__':
    unittest.main()
