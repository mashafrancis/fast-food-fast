"""
Handles data storage for all orders and users
"""
import jwt
from datetime import datetime, timedelta

from flask import jsonify, current_app
from flask_restful import fields, marshal
from werkzeug.security import generate_password_hash, check_password_hash

all_users = [{
    "user_id": "1",
    "username": "admin",
    "email": "admin@gmail.com",
    "password": generate_password_hash("admin1234")}]

order_count = 1

all_orders = []

order_fields = {
    'order_id': fields.Integer,
    'name': fields.String,
    'quantity': fields.String,
    'price': fields.String,
    'status': fields.String,
    'uri': fields.Url('orders')
}


class User(object):
    """This contains methods for the users"""

    def __init__(self, username, email, password, confirm_password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.confirm_password = confirm_password
        self.user_id = len(all_users) + 1

    def __repr__(self):
        return "<User: {}>".format(self.username)

    def validate_password(self, password):
        """Validate password during login."""
        return check_password_hash(self.password, password)

    @staticmethod
    def generate_token(user_id):
        """Generates authentication token."""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create byte string token using payload and secret key
            jwt_string = jwt.encode(
                payload,
                current_app.config['SECRET'],
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decode the access token from the authorization."""
        try:
            payload = jwt.decode(token, current_app.config['SECRET'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Not Authorized please login!"
        except jwt.InvalidTokenError:
            return "Not Authorized.Please Register or Login"

    def json(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    def add_one(self):
        """Adds user to the list"""
        user = {'user_id': self.user_id,
                'username': self.username,
                'email': self.email,
                'password': self.password}
        all_users.append(user)
        return jsonify({'users': all_users})

    @staticmethod
    def get_all():
        """Gets all users"""
        return all_users

    @classmethod
    def filter_by_id(cls, user_id):
        """Filter different queries"""
        return [user for user in all_users if user['user_id'] == user_id]

    @classmethod
    def filter_by_username(cls, username):
        return [user for user in all_users if user['username'] == username]

    @classmethod
    def filter_by_email(cls, email):
        return [user for user in all_users if user['email'] == email]

    @staticmethod
    def delete(user_id):
        """Deletes a user"""
        user = User.filter_by_id(user_id)
        all_users.remove(user[0])
        return user

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an email/password (sent from the site form) is valid
        Checks that the email exists and password is correct
        :param email: The user's email
        :param password: The sha512 hashed password
        :return: True if valid, False otherwise
        """
        # Password in sha512 -> pbkdf2_sha512
        user = User.filter_by_email(email)
        hash_password = (users['password'] for users in user)
        if user:
            check_password_hash(hash_password, password)
        return True


class Order(object):
    """
    This contains the methods to add, update and delete an order
    """

    def save(self):
        """Creates an order and appends this information to orders dictionary"""
        pass

    @classmethod
    def update(cls, order_id, name, quantity, price, status):
        """Updates the order information"""
        pass

    @staticmethod
    def get_all():
        """Gets all the orders saved"""
        return [marshal(order, order_fields) for order in all_orders]

    @staticmethod
    def get_by_id(order_id):
        """Get a single order by its id"""
        return [order for order in all_orders if order['order_id'] == order_id]

    @staticmethod
    def delete(order_id):
        """Deletes a single order"""
        order = Order.get_by_id(order_id)
        all_orders.remove(order[0])
        return order
