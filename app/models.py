from datetime import datetime, timedelta

import jwt
from flask import current_app
from passlib.handlers.pbkdf2 import pbkdf2_sha512

from app.database import Database
from app.utils import Savable, Utils


class User(Savable):
    collection = 'users'

    def __init__(self, email, password, user_id, **kwargs):
        super(User, self).__init__(**kwargs)
        self.email = email
        self.password = password
        self.user_id = user_id

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'password': self.password
        }

    def add_user(self):
        """Adds user to the list"""
        user = User(self.email,
                    Utils.hash_password(self.password),
                    self.user_id)
        user.save_user()

    @staticmethod
    def list_all_users():
        users = Database.find_all(User.collection)
        return users

    @classmethod
    def find_by_email(cls, email):
        finder = (lambda x: x['email'] == email)
        return Database.find_one(User.collection, finder)

    @classmethod
    def find_by_id(cls, user_id):
        finder = (lambda x: x['user_id'] == user_id)
        return Database.find_one(User.collection, finder)

    @classmethod
    def find_by_username(cls, username):
        finder = (lambda x: x['username'] == username)
        return Database.find_one(User.collection, finder)

    @staticmethod
    def delete(user_id):
        finder = (lambda x: x['user_id'] != user_id)
        return Database.remove(User.collection, finder)

    @staticmethod
    def hash_password(password):
        """
        Hashes the password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512 -> pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.hash(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checked that the password the user sent matches that of the database.
        The database password is encrypted more than the user's password at the stage
        :param password: sha512-ashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if passwords match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)

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


class Admin(User):
    def __init__(self, username, password, access):
        super(Admin, self).__init__(username, password)
        self.access = access

    def __repr__(self):
        return f'<Admin {self.email}, access {self.access}>'

    def to_dict(self):
        return {
            'password': self.password,
            'access': self.access
        }


class Orders(Savable):
    collection = 'orders'

    def __init__(self, order_id, name, quantity, price, date_created, created_by, status):
        self.order_id = order_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.date_created = date_created
        self.created_by = created_by
        self.status = status

    def __repr__(self):
        return f'<Order {self.name}>'

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price,
            'date_created': self.date_created,
            'created_by': self.created_by,
            'status': self.status
        }

    def add_order(self):
        """Adds user to the list"""
        order = Orders(self.order_id,
                       self.name,
                       self.quantity,
                       self.price,
                       self.date_created,
                       self.created_by,
                       self.status)
        order.save_order()
        return self.to_dict()

    @staticmethod
    def list_all_orders():
        users = Database.find_all(Orders.collection)
        return users

    @classmethod
    def find_by_id(cls, order_id):
        finder = (lambda x: x['order_id'] == order_id)
        return Database.find_one(Orders.collection, finder)

    @staticmethod
    def delete(order_id):
        finder = (lambda x: x['order_id'] == order_id)
        return Database.remove(Orders.collection, finder)

    @staticmethod
    def delete_all():
        return Database.remove_all(Orders.collection)
