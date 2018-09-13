import os
import sys  # Fix import errors

from .base_test import BaseTests
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TokenTestCase(BaseTests):
    def test_no_token(self):
        response = self.client().post('/v1/orders', data=self.order)
        return response

