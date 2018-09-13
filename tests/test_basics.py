import unittest

from flask import current_app
from app import create_app

from .base_test import BaseTests


class BasicsTestCase(BaseTests):
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(create_app('testing'))


if __name__ == '__main__':
    unittest.main()
