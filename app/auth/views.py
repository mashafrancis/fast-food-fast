import re

from flask import request, jsonify, make_response, session
from flask.views import MethodView

from app.auth import auth
from app.database import Database
from app.models import User
from app.responses.responses import Error, Success, Response
from app.utils import Utils


class RegistrationView(MethodView):
    """This class-based view registers a new user and fetches all user."""
    def __init__(self):
        super().__init__()
        self.error = Error()
        self.success = Success()
        self.response = Response()

    def post(self):
        """API POST Requests for this view. Url ---> /v1/auth/register"""

        data = request.get_json(force=True)
        email = str(data['email']).lower()
        password = data['password']
        confirm_password = data['confirm_password']
        user_id = Database.user_count() + 1

        if email and password and confirm_password:
            if not Utils.email_is_valid(email):
                return self.error.bad_request('Your email is invalid! '
                                              'Kindly provide use with the right email address format')

            if not re.match(r"^(?=.*[a-z])(?=.*[0-9]){6}", password):
                return self.error.bad_request('Password must contain: '
                                              'lowercase letters, at least a digit, and a min-length of 6')

            if confirm_password != password:
                return self.error.bad_request('Your password must match!')

            user = User.find_by_email(email)
            if not user:
                user = User(email=email,
                            password=password,
                            user_id=user_id)
                user.add_user()
                return self.success.create_resource('User {} successfully registered'.format(user.email))
            else:
                return self.error.causes_conflict('User already exists! Please login.')
        else:
            if not email:
                return self.error.bad_request('Please provide email!')
            else:
                return self.error.bad_request('Please provide password!')

    def get(self):
        """API GET Requests for this view. Url ---> /v1/auth/register"""
        results = []
        users = User.list_all_users()
        if users:
            for users in users:
                obj = self.response.define_users(users)
                results.append(obj)
            return self.success.complete_request(results)
        else:
            return self.error.not_found('No users to display!')


class LoginView(MethodView):
    """This class-based view handles user login and access token generation"""

    def __init__(self):
        super().__init__()
        self.error = Error()
        self.success = Success()
        self.response = Response()

    def post(self):
        """API POST Requests for this view. Url ---> /v1/auth/login"""
        try:
            data = request.get_json(force=True)
            password = data['password']
            email = data['email']

            if not email:
                return self.error.bad_request('Your email is missing!')

            user = User.find_by_email(email)
            if user:
                if email and password:
                    if Utils.check_hashed_password(password, user[0]['password']):
                        access_token = User.generate_token(user[0]['user_id'])
                        if access_token:
                            response = {
                                'message': 'You have logged in successfully.',
                                'access_token': access_token.decode()}
                            return make_response(jsonify(response)), 200
                    else:
                        return self.error.bad_request('Password mismatch!')
                else:
                    if not password:
                        return self.error.bad_request('Your password is missing!')

            return self.error.unauthorized('User does not exist. Kindly register!')
        except Exception as e:
            # Create a response containing a string error message
            return self.error.internal_server_error(str(e))


registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')

auth.add_url_rule('/v1/auth/register',
                  view_func=registration_view,
                  methods=['POST', 'GET'])

auth.add_url_rule('/v1/auth/login',
                  view_func=login_view,
                  methods=['POST', 'GET'])
