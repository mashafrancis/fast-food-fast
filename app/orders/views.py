from flask import Blueprint, abort
from flask_restful import Resource, Api, reqparse, marshal

from app.models import Order, all_orders, order_fields


class OrderList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True, help='Name not provided', location='json')
        self.reqparse.add_argument('quantity', type=int, required=True, help='Quantity not provided', location='json')
        self.reqparse.add_argument('price', type=float, required=True, help='Price not provided', location='json')
        self.reqparse.add_argument('status', type=str, default="Pending", location='json')
        super(OrderList, self).__init__()

    def get(self):
        if len(all_orders) == 0:
            return {'status': 'success',
                    'message': 'No orders available!'}
        else:
            return {'status': 'success',
                    'orders': [marshal(order, order_fields) for order in all_orders]}

    def post(self):
        args = self.reqparse.parse_args()
        order = {
            'order_id': len(all_orders) + 1,
            'name': args['name'],
            'quantity': args['quantity'],
            'price': args['price'],
            'status': args['status']
        }
        all_orders.append(order)
        return {'status': 'your order successfully added',
                'order': marshal(order, order_fields)}, 201


class Orders(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=False, location='json')
        self.reqparse.add_argument('quantity', type=int, required=False, location='json')
        self.reqparse.add_argument('price', type=int, required=False, location='json')
        self.reqparse.add_argument('status', type=str, location='json')
        super(Orders, self).__init__()

    def get(self, order_id):
        order = [order for order in all_orders if order['order_id'] == order_id]
        if len(order) == 0:
            abort(404, 'Order {} not found!'.format(order_id))
        return {'order': marshal(order[0], order_fields)}, 200

    def put(self, order_id):
        order = [order for order in all_orders if order['order_id'] == order_id]
        if len(order) == 0:
            abort(404, 'Order {} not found!'.format(order_id))
        order = order[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                order[k] = v
            return {'order': marshal(order, order_fields)}, 200

    @staticmethod
    def delete(order_id):
        order = [order for order in all_orders if order['order_id'] == order_id]
        if len(order) == 0:
            abort(404, 'Order {} not found!'.format(order_id))
        return {'status': 'success',
                'message': 'the order has been removed successfully'}, 200


orders_api = Blueprint('resources.orders', __name__)
api = Api(orders_api)
api.add_resource(OrderList, '/v1/orders', endpoint='orders')
api.add_resource(Orders, '/v1/orders/<int:order_id>', endpoint='order')
