from flask import make_response, jsonify, request
from flask_restful import Resource
from jsonschema import validate, ValidationError

from app.models import Order
from app.schemas import Order_Schema


class Orders(Resource):
    """Contains GET and POST methods"""
    def post(self):
        """POST request to adds a new order"""
        data = request.json
        try:
            validate(data, Order_Schema)
            new_order = Order(data['name'], data['quantity'], data['price'])
            result = new_order.save()
            return make_response(jsonify(result), 201)
        except ValidationError as error:
            return {'error': str(error)}, 400

    @staticmethod
    def get():
        """GET request to fetch all orders"""
        return make_response(jsonify(Order.get_all()), 200)

