from flask import make_response, jsonify, request
from flask_restful import Resource, reqparse
from jsonschema import validate, ValidationError

from app.models import Order
from app.schemas import Order_Schema


class OrderList(Resource):
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


class Orders(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single ride"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name', required=True, type=str,
            help='Kindly input your order',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'quantity', required=True, type=str,
            help='Kindly input your order',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'price', required=True, type=str,
            help='Kindly input your order',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'status', type=str,
            help='Kindly input your order',
            location=['form', 'json'])
        super().__init__()

    @staticmethod
    def get(order_id):
        """GET request to fetch a particular order"""
        try:
            order = Order.get_by_id(order_id)
            return make_response(jsonify(order), 200)
        except KeyError:
            return make_response(jsonify({"message": "order does not exist"}), 404)

    def put(self, order_id):
        """PUT request to update a particular order"""
        kwargs = self.reqparse.parse_args()
        result = Order.update(order_id, **kwargs)
        if result == {"message": "order does not exist"}:
            return make_response(jsonify(result), 404)
        return make_response(jsonify(result), 200)

    @staticmethod
    def delete(order_id):
        """DELETE request to remove a particular order"""
        return Order.delete(order_id)
