import re

import requests
from flask import request, jsonify, make_response

from app.auth import auth
from app.models import User


@auth.route('/v1/auth/register', methods=['POST', 'GET'])
def register():
    """API POST and GET Requests"""
    if request.method == 'POST':
        data = request.get_json(force=True)
        username = str(data['username']).lower()
        email = str(data['email']).lower()
        password = data['password']
        confirm_password = data['confirm_password']

        if username and email and password and confirm_password:
            if not re.match(r"(?=^.{3,}$)(?=.*[a-z])^[A-Za-z0-9_-]+( +[A-Za-z0-9_-]+)*$", username):
                response = \
                    jsonify({'message':
                             'Username must contain at least 1 letter and other characters with a minimum length of 4'})
                response.status_code = 400
                return response

            if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
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

            user = User.filter_by_email(email)
            if not user:
                if not User.filter_by_username(username):
                    user = User(username=username, email=email, password=password, confirm_password=confirm_password)
                    user.add_one()
                    response = {'message': 'User {} successfully registered'.format(user.email)}
                    return make_response(jsonify(response)), 201
                else:
                    response = {'message': 'User with that username already exist.'}
                    return make_response(jsonify(response)), 409
            else:
                response = {'message': 'User with that email already exist.'}
                return make_response(jsonify(response)), 409

        else:
            if not username:
                response = jsonify({'message': 'Please provide username!'})
                response.status_code = 400
                return response
            elif not email:
                response = jsonify({'message': 'Please provide email!'})
                response.status_code = 400
                return response
            else:
                response = jsonify({'message': 'Please provide password!'})
                response.status_code = 400
                return response

    else:
        users = User.get_all()
        if users is None:
            response = jsonify({'message': 'No users to display!'})
            response.status_code = 404
            return response
        else:
            response = users
            response.status_code = 200
            return response
