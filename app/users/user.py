from datetime import datetime, timedelta

import jwt
from flask import current_app, jsonify, make_response
from werkzeug.security import check_password_hash, generate_password_hash

from ..database import Database
from ..utils import Savable


class User(Savable):
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
        user.save()

    @staticmethod
    def list_all_users():
        users = Database.get_all_users()
        return users

    @classmethod
    def find_by_email(cls, email):
        return Database.find(lambda x: x['email'] == email)

    @classmethod
    def find_by_id(cls, user_id):
        return Database.find(lambda x: x['user_id'] == user_id)

    @classmethod
    def find_by_username(cls, username):
        return Database.find(lambda x: x['username'] == username)

    @staticmethod
    def delete():
        return Database.remove(lambda x: x['user_id'] != 'user_id')

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
