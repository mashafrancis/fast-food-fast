from flask import jsonify, make_response


class Response:
    """API Responses customized"""
    def __init__(self):
        self.ok_status = 200
        self.created_status = 201
        self.bad_request_status = 400
        self.unauthorized_status = 401
        self.forbidden_status = 403
        self.not_found_status = 404
        self.not_acceptable_status = 406
        self.conflict_status = 409
        self.internal_server_error_status = 500

    @staticmethod
    def define_orders(order):
        """Return a dictionary of the orders object"""
        obj = {
            'order_id': order['order_id'],
            'name': order['name'],
            'quantity': order['quantity'],
            'price': order['price'],
            'date_created': order['date_created'],
            'created_by': order['created_by'],
            'status': order['status']
        }
        return obj

    @staticmethod
    def define_users(user):
        """Return a dictionary of the users object"""
        obj = {
            'user_id': user['user_id'],
            'email': user['email'],
            'password': user['password']
        }
        return obj


class Success(Response):
    """For successful requests"""

    def complete_request(self, message):
        """For a successful request"""
        response = jsonify({"message": message})
        return make_response(response), self.ok_status

    def create_resource(self, resource):
        """ Creation of any Resource """
        response = jsonify({"message": resource})
        return make_response(response), self.created_status


class Error(Response):
    """For error requests"""

    def not_found(self, message):
        """ Resource not found in User domain """
        response = jsonify({"error": message})
        return make_response(response), self.not_found_status

    def not_acceptable(self, message):
        """ Request has been understood but not accepted """
        response = jsonify({"error": message})
        return make_response(response), self.not_acceptable_status

    def causes_conflict(self, message):
        """ Request made causes conflict """
        response = jsonify({"error": message})
        return make_response(response), self.conflict_status

    def unauthorized(self, message):
        """ Request has an invalid token """
        response = jsonify({"error": message})
        return make_response(response), self.unauthorized_status

    def forbid_action(self, message):
        """ Request made requires a token, none provided """
        response = jsonify({"error": message})
        return make_response(response), self.forbidden_status

    def bad_request(self, message):
        """ Request made in the wrong format """
        response = jsonify({"error": message})
        return make_response(response), self.bad_request_status

    def internal_server_error(self, message):
        """ An error that was not anticipated """
        response = jsonify({"error": message})
        return make_response(response), self.internal_server_error_status
