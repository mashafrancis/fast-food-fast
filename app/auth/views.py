import re

from flask import request, jsonify, make_response
from flask.views import MethodView

from app.auth import auth
from app.models import User
from app.utils import Utils


class RegistrationView(MethodView):
    """This class-based view registers a new user and fetches all user."""

    @staticmethod
    def post():
        """API POST Requests for this view. Url ---> /v1/auth/register"""

        data = request.get_json(force=True)
        email = str(data['email']).lower()
        password = data['password']
        confirm_password = data['confirm_password']

        if email and password and confirm_password:
            if not Utils.email_is_valid(email):
                response = \
                    jsonify({'message':
                                 'Your email is invalid! Kindly provide use with the right email address format'})
                response.status_code = 400
                return response

            if not re.match(r"^(?=.*[a-z])(?=.*[0-9]){6}", password):
                response = \
                    jsonify({'message':
                                 'Password must contain: lowercase letters, at least a digit, and a min-length of 6'})
                response.status_code = 400
                return response

            if confirm_password != password:
                response = jsonify({'message': 'Your password must match!'})
                response.status_code = 400
                return response

            user = User.find_by_email(email)
            if not user:
                user = User(email=email,
                            password=password)
                user.add_user()
                response = {'message': 'User {} successfully registered'.format(user.email)}
                return make_response(jsonify(response)), 201
            else:
                response = {'message': 'User already exists! Please login.'}
                return make_response(jsonify(response)), 409

        else:
            if not email:
                return make_response(jsonify({'message': 'Please provide email!'}), 400)

            else:
                return make_response(jsonify({'message': 'Please provide password!'}), 400)

    @staticmethod
    def get():
        """API GET Requests for this view. Url ---> /v1/auth/register"""
        results = []
        users = User.list_all_users()
        if users:
            for users in users:
                obj = {
                    'email': users['email'],
                    'password': users['password']
                }
                results.append(obj)
            return make_response(jsonify(results), 200)
        else:
            return make_response(jsonify({'message': 'No users to display!'}), 404)


class LoginView(MethodView):
    """This class-based view handles user login and access token generation"""

    def post(self):
        """API POST Requests for this view. Url ---> /v1/auth/login"""
        try:
            data = request.get_json(force=True)
            password = data['password']
            email = data['email']

            u = User(email=email, password=password)
            result = u.login(email, password)
            return result
        except Exception as e:
            # Create a response containing a string error message
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500


registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')

auth.add_url_rule('/v1/auth/register',
                  view_func=registration_view,
                  methods=['POST', 'GET'])

auth.add_url_rule('/v1/auth/login',
                  view_func=login_view,
                  methods=['POST', 'GET'])
