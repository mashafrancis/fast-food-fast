from functools import wraps

from flask import request, make_response, jsonify

from app.api.v1.models.blacklist import BlackList
from app.api.v1.models.user import User


def user_required(f):
    """Checks for valid token for a registered user in the header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return make_response(jsonify({
                'error': 'Login to get authorized. If you had logged in, your session expired.'}), 401)
        else:
            token = auth_header.split("Bearer ")
            access_token = token[0]
            access_token = access_token.encode()
            if access_token:
                blacklisted = BlackList.check_token(access_token)
                if not blacklisted:
                    user_id = User.decode_token(access_token)
                    if not isinstance(user_id, str):
                        user_id = user_id
                    else:
                        return make_response(jsonify({'message': user_id}), 201)
                else:
                    return make_response(jsonify({'error': 'Invalid token!'}), 401)
            else:
                return make_response(jsonify({'error': 'No access token!'}), 401)
        return f(user_id=user_id, *args, **kwargs)
    return decorated


def admin_required(f):
    """Checks for valid token for an admin in the header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return make_response(jsonify({
                'error': 'Login as admin to get authorized. If you had logged in, your session expired.'}), 401)
        else:
            token = auth_header.split("Bearer ")
            access_token = token[1]
            access_token = access_token.encode()
            if access_token:
                blacklisted = BlackList.check_token(access_token)
                if not blacklisted:
                    user_id = User.decode_token(access_token)
                    if not isinstance(user_id, str):
                        user_id = user_id
                    else:
                        return make_response(jsonify({'message': user_id}), 201)
                else:
                    return make_response(jsonify({'error': 'Invalid token!'}), 401)
            else:
                return make_response(jsonify({'error': 'No access token!'}), 401)
        return f(user_id=user_id, *args, **kwargs)
    return decorated
