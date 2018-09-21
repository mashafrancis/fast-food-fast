from flask import request, Blueprint
from flask.views import MethodView

from app.api.v1.models.blacklist import BlackList
from app.api.v1.models.user import User
from app.responses import Error, Success, Response, Auth
from app.api.v1.utils import Utils

auth = Blueprint('auth', __name__)


class RegistrationView(MethodView):
    """This class-based view registers a new user and fetches all user."""
    def __init__(self):
        super().__init__()
        self.error = Error()
        self.success = Success()
        self.response = Response()

    def post(self):
        """API POST Requests for this view. Url ---> /v1/auth/register"""
        try:
            if request.content_type == 'application/json':
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
                        return self.success.create_resource('User {} successfully registered'.format(user.email))
                    return self.error.causes_conflict('User already exists! Please login.')
                else:
                    if not email:
                        return self.error.bad_request('Please provide email!')
                    elif not password:
                        return self.error.bad_request('Please provide password!')
                    return self.error.bad_request('Please confirm password!')
            return self.error.bad_request('Content-type must be JSON!')
        except Exception as e:
            # Create a response containing a string error message
            return self.error.internal_server_error(str(e))


class LoginView(MethodView):
    """This class-based view handles user login and access token generation"""

    def __init__(self):
        super().__init__()
        self.auth = Auth()
        self.error = Error()
        self.success = Success()
        self.response = Response()

    def post(self):
        """API POST Requests for this view. Url ---> /v1/auth/login"""
        try:
            if request.content_type == 'application/json':
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
                                return self.auth.create_resource(message='You have logged in successfully!',
                                                                 token=access_token.decode())
                        else:
                            return self.error.bad_request('Wrong Password!')
                    else:
                        if not password:
                            return self.error.bad_request('Your password is missing!')
                return self.error.unauthorized('User does not exist. Kindly register!')
            return self.error.bad_request('Content-type must be JSON!')
        except Exception as e:
            # Create a response containing a string error message
            return self.error.internal_server_error(str(e))


class LogoutView(MethodView):
    def __init__(self):
        super().__init__()
        self.auth = Auth()
        self.error = Error()
        self.success = Success()
        self.response = Response()

    def post(self):
        # Retrieve token
        try:
            header_auth = request.headers.get('Authorization', None)

            if header_auth:
                try:
                    access_token = header_auth.split(" ")[1]
                except IndexError:
                    return self.error.unauthorized('Please provide a valid access_token!')
                else:
                    access_token = header_auth.split(" ")[1]
                    if access_token:
                        decoded_token = User.decode_token(access_token)
                        if not isinstance(decoded_token, str):
                            token_invalid = BlackList(access_token)
                            token_invalid.save()
                            return self.success.ok_status('You have been logged out successfully!')
                        return self.error.bad_request(decoded_token)
                    return self.error.unauthorized('Invalid token!')
        except Exception as e:
            # Create a response containing a string error message
            return self.error.internal_server_error(str(e))


registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')

auth.add_url_rule('auth/register',
                  view_func=registration_view,
                  methods=['POST'])

auth.add_url_rule('auth/login',
                  view_func=login_view,
                  methods=['POST'])

auth.add_url_rule('auth/logout',
                  view_func=logout_view,
                  methods=['POST'])
