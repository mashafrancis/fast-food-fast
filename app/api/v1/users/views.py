from flask.views import MethodView

from app.api.v1.models.user import User
from app.api.v1.users import user
from app.responses import Auth, Error, Success, Response


class UsersView(MethodView):
    """This class-based view handles user login and access token generation"""

    def __init__(self):
        super().__init__()
        self.auth = Auth()
        self.error = Error()
        self.success = Success()
        self.response = Response()

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


class UserView(MethodView):
    def __init__(self):
        super().__init__()
        self.auth = Auth()
        self.error = Error()
        self.success = Success()
        self.response = Response()

    def get(self, user_id):
        """Endpoint for fetching a particular order."""
        _user = User.find_by_id(user_id)
        if not _user:
            return self.error.not_found("Sorry, User ID No {} does't exist!".format(user_id))
        return self.success.complete_request(_user)


users_view = UsersView.as_view('users_view')
user_view = UserView.as_view('user_view')

user.add_url_rule('users',
                  view_func=users_view,
                  methods=['GET'])

user.add_url_rule('users/<int:user_id>',
                  view_func=user_view,
                  methods=['GET'])
