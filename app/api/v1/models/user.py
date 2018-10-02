from datetime import datetime, timedelta

import jwt
from flask import current_app
from passlib.handlers.pbkdf2 import pbkdf2_sha512

import app.responses as UserErrors

from app.data import Database
from app.api.v1.common.utils import Savable, Utils


class User(Savable):
    collection = 'users'

    def __init__(self, username, email, password):
        super().__init__()
        self.username = username
        self.email = email
        self.password = password
        self.user_id = Database.user_count() + 1
        self.date_registered = datetime.now()
        if self.email == current_app.config['FAST_FOOD_ADMIN']:
            self.role = 'admin'
        else:
            self.role = 'user'

    def __repr__(self):
        return f'<User {self.email}'

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'date_registered': self.date_registered
        }

    @staticmethod
    def validate_register_details(email, username, password, confirm_password):
        """
        This method register a user using email and password.
        The password already comes hashed as sha-512
        :param confirm_password: User has to confirm password
        :param username: User's username
        :param email: User's email (might be invalid)
        :param password: sha512-hashed password
        :return: True if registered successfully, or False otherwise
        """
        if email and username and password and confirm_password:
            if not Utils.email_is_valid(email):
                raise UserErrors.BadRequest("Your email is invalid! "
                                            "Kindly provide use with the right email address format")
            if not Utils.username_checker(username):
                raise UserErrors.BadRequest("Username must contain at least letter; "
                                            "plus other letters or digits and with a min length of 3")
            if User.find_by_username(username):
                raise UserErrors.Conflict('Username already exists! Kindly choose another.')
            if not Utils.password_checker(password):
                raise UserErrors.BadRequest("Password must contain: "
                                            "lowercase letters, atleast a digit, and a min-length of 6")
            if confirm_password != password:
                raise UserErrors.BadRequest('Your password must match!')

        else:
            if not username:
                raise UserErrors.BadRequest('Please provide username!')
            if not email:
                raise UserErrors.BadRequest('Please provide email!')
            if not password:
                raise UserErrors.BadRequest('Please provide password!')
            if not confirm_password:
                raise UserErrors.BadRequest('Please confirm password!')

        return True

    def add_user(self):
        """Adds user to the list"""
        user = User(self.username,
                    self.email,
                    Utils.hash_password(self.password))
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
        """
        Generates authentication token.
        :param user_id:
        :return: string
        """
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
    def decode_token(access_token):
        """
        Decode the access token from the authorization.
        :param access_token:
        :return: integer or string
        """
        try:
            payload = jwt.decode(access_token, current_app.config['SECRET'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Signature Expired. Please login!"
        except jwt.InvalidTokenError:
            return "Invalid Token. Please Register or Login"
