"""
Handles data storage for all orders and users
"""
from flask import jsonify, request
from flask_restful import fields, marshal
from werkzeug.security import generate_password_hash, check_password_hash


all_users = [{
    "user_id": "1",
    "username": "admin",
    "email": "admin@gmail.com",
    "password": generate_password_hash("admin1234", method='sha256')}
]

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
        self.password = password
        self.confirm_password = confirm_password
        self.user_id = len(all_orders) + 1

    def json(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    @staticmethod
    def add_one():
        """Adds user to the list"""
        user = {'user_id': len(all_users) + 1,
                'username': request.json['username'],
                'email': request.json['email'],
                'password': request.json['password']}
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

    def verify_password(self, password):
        """Validates password during login"""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User: {}".format(self.username)


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
