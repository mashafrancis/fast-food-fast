from flask import abort
from flask_restful import Resource, reqparse, marshal

from app.models import Order, all_orders, order_fields


class OrderList(Resource):
    """Contains GET and POST methods"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True, help='Name not provided', location='json')
        self.reqparse.add_argument('quantity', type=str, required=True, help='Quantity not provided', location='json')
        self.reqparse.add_argument('price', type=str, required=True, help='Price not provided', location='json')
        self.reqparse.add_argument('status', type=str, default="Pending", location='json')
        super(OrderList, self).__init__()

    def get(self):
        """
        Endpoint fetching all orders
        ---
        tags:
          -  Orders
        responses:
          200:
            description: All orders made
            schema:
              Orders: Orders
              properties:
                Orders:
                  type: object
                  schema:
                   $ref: '#/definition/Orders'
        """
        orders = Order.get_all()
        if len(all_orders) == 0:
            return {'status': 'success',
                    'message': 'No orders available!'}
        else:
            return {'status': 'success',
                    'orders': orders}

    def post(self):
        """
        Endpoint for adding a new order
        ---
        tags:
          -  Orders
        parameters:
          - name: name
            required: true
            in: formData
            type: string
          - name: quantity
            required: true
            in: formData
            type: string
          - name: price
            required: true
            in: formData
            type: string
          - name: status
            required: false
            in: formData
            type: string
        responses:
          201:
            description: Your order has been added successfully.
            schema:
              $ref: '#/definition/Orders'
        """
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

    @staticmethod
    def delete():
        """
        Endpoint for deleting all orders
        ---
        tags:
          -  Orders
        """
        if len(all_orders) == 0:
            return {'message': 'No orders available!'}
        else:
            all_orders.clear()
            return {'status': 'all your orders have been successfully deleted'}


class Orders(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single ride"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=False, location='json')
        self.reqparse.add_argument('quantity', type=str, required=False, location='json')
        self.reqparse.add_argument('price', type=str, required=False, location='json')
        self.reqparse.add_argument('status', type=str, location='json')
        super(Orders, self).__init__()

    def get(self, order_id):
        """
        Endpoint for fetching a particular order.
        ---
        tags:
          -  Order List
        parameters:
          - name: order_id
            in: path
            type: integer
            required: true
            description: The ID of the order, try 1!
        responses:
          200:
            description: The order data
            schema:
              $ref: '#/definition/Orders'
        """
        order = self.abort_if_order_doesnt_exist(order_id)
        return {'order': marshal(order[0], order_fields)}, 200

    def put(self, order_id):
        """
        Endpoint for updating a particular order
        ---
        tags:
          -  Order List
        parameters:
          - name: order_id
            required: true
            in: path
            type: integer
            description: The ID of the order, try 1!
          - name: name
            required: true
            in: formData
            type: string
          - name: quantity
            required: true
            in: formData
            type: string
          - name: price
            required: true
            in: formData
            type: string
          - name: status
            required: false
            in: formData
            type: string
        responses:
          200:
            description: The Order has been updated
            schema:
              $ref: '#/definition/Orders'
        """
        order = self.abort_if_order_doesnt_exist(order_id)
        order = order[0]
        args = self.reqparse.parse_args()
        order.update(args)
        return {'order': marshal(order, order_fields)}, 200

    def delete(self, order_id):
        """
        Endpoint for removing a particular order
        ---
        tags:
          -  Order List
        parameters:
          - name: order_id
            in: path
            type: integer
            required: true
            description: The ID of the order, try 1!
        responses:
          200:
            description: Order has been removed
        """
        order = self.abort_if_order_doesnt_exist(order_id)
        all_orders.remove(order[0])
        return {'status': 'success',
                'message': 'the order has been removed successfully'}, 200

    @classmethod
    def abort_if_order_doesnt_exist(cls, order_id):
        order = [order for order in all_orders if order['order_id'] == order_id]
        if len(order) == 0:
            abort(404, 'Order {} not found!'.format(order_id))
        return order
