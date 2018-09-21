from flask import request, Blueprint, make_response, jsonify
from flask.views import MethodView

from app.api.v1.models.blacklist import BlackList
from app.api.v1.models.user import User
from app.responses import Error, Success, Response, Auth
from app.api.v1.common.utils import Utils

auth = Blueprint('auth', __name__)


class Responses:
    def __init__(self):
        super().__init__()
        self.error = Error()
        self.success = Success()
        self.response = Response()
        self.auth = Auth()


class RegistrationView(MethodView, Responses):
    """This class-based view registers a new user and fetches all user."""

    def post(self):
        """API POST Requests for this view. Url ---> /v1/auth/register"""
        try:
            data = request.get_json(force=True)
            email = str(data['email']).lower()
            password = data['password']
            confirm_password = data['confirm_password']

            if email and password and confirm_password:
                if not Utils.email_is_valid(email):
                    return self.error.bad_request('Your email is invalid! '
                                                  'Kindly provide use with the right email address format')

                if not Utils.password_checker(password):
                    return self.error.bad_request('Password must contain: '
                                                  'lowercase letters, at least a digit, and a min-length of 6')

                if confirm_password != password:
                    return self.error.bad_request('Your password must match!')

                user = User.find_by_email(email)
                if not user:
                    user = User(email=email, password=password)
                    user.add_user()
                    # generate access_token for user
                    access_token = user.generate_token(user.user_id)
                    return self.auth.create_resource(
                        message='User {} successfully registered'.format(user.email),
                        token=access_token.decode())
                return self.error.causes_conflict('User already exists! Please login.')
            else:
                if not email:
                    return self.error.bad_request('Please provide email!')
                elif not password:
                    return self.error.bad_request('Please provide password!')
                return self.error.bad_request('Please confirm password!')
        except Exception as e:
            # Create a response containing a string error message
            return self.error.internal_server_error(str(e))


class LoginView(MethodView, Responses):
    """This class-based view handles user login and access token generation"""

    def post(self):
        """API POST Requests for this view. Url ---> /v1/auth/login"""
        try:
            data = request.get_json(force=True)
            password = data['password']
            email = data['email']

            if not email:
                return self.error.bad_request('Your email is missing!')

            if not Utils.email_is_valid(email):
                return self.error.unauthorized('Your email is invalid! Kindly recheck your email.')

            user = User.find_by_email(email)
            if user:
                if email and password:
                    if Utils.check_hashed_password(password, user[0]['password']):
                        access_token = User.generate_token(user[0]['user_id'])
                        if access_token:
                            return self.auth.complete_request(message='You have logged in successfully!',
                                                              token=access_token.decode())
                    else:
                        return self.error.bad_request('Wrong Password!')
                else:
                    if not password:
                        return self.error.bad_request('Your password is missing!')
            return self.error.not_found('User does not exist. Kindly register!')
        except Exception as e:
            # Create a response containing a string error message
            return self.error.internal_server_error(str(e))


class ProfileView(MethodView, Responses):
    """This class handles the user resource"""

    def get(self):
        header_auth = request.headers.get('Authorization', None)
        if not header_auth:
            return self.error.unauthorized(
                'Login to view your profile!.')
        else:
            token = header_auth.split("Bearer ")
            access_token = token[1]
            access_token = access_token.encode()
            if access_token:
                response = User.decode_token(access_token)
                if not isinstance(response, str):
                    user = User.find_by_id(user_id=response)
                    return self.success.complete_request(user)
                return self.error.unauthorized(response)
            return self.error.unauthorized('No access token!')
            # return self.success.complete_request(user)


class LogoutView(MethodView, Responses):
    """This class handles the user logout resource"""

    def post(self):
        # Retrieve token
        header_auth = request.headers.get('Authorization', None)

        if not header_auth:
            return self.error.internal_server_error('No token provided!')
        else:
            token = header_auth.split(" ")
            access_token = token[1]
            if not access_token:
                return self.error.unauthorized('Invalid token!')
            else:
                user = User.decode_token(access_token)
                if not isinstance(user, str):
                    invalid_token = BlackList(access_token)
                    invalid_token.save_blacklist()
                    return self.success.complete_request('You have been logged out successfully!')
                else:
                    return self.error.unauthorized(user)


registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')
user_view = ProfileView.as_view('user_view')
logout_view = LogoutView.as_view('logout_view')

auth.add_url_rule('auth/register',
                  view_func=registration_view,
                  methods=['POST'])

auth.add_url_rule('auth/login',
                  view_func=login_view,
                  methods=['POST'])

auth.add_url_rule('auth/profile',
                  view_func=user_view,
                  methods=['GET'])

auth.add_url_rule('auth/logout',
                  view_func=logout_view,
                  methods=['POST'])
