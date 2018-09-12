from datetime import datetime, timedelta

import jwt
from flask import current_app, jsonify, make_response
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import Database
from app.utils import Savable


class User(Savable):
    collection = 'users'

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)
        self.user_id = Database.user_count() + 1

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
                    self.password)
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

    def login(self, email, password):
        """Login registered users"""
        user = User.find_by_email(email)
        if user:
            if check_password_hash(self.password, password):
                access_token = User.generate_token(self.user_id)
                if access_token:
                    response = {
                        'message': 'You have logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = jsonify({
                    'message': 'Incorrect password!'})
                response.status_code = 404
                return response
        else:
            response = jsonify({
                'message': 'Invalid email or password. Please try again!'})
            response.status_code = 401
            return response


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
