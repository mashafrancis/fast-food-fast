"""
Handles data storage for all orders and users
"""
from flask import make_response, jsonify, abort
from flask_restful import fields

order_count = 1

all_orders = []

order_fields = {
    'order_id': fields.Integer,
    'name': fields.String,
    'quantity': fields.Integer,
    'price': fields.Float,
    'status': fields.String,
    'uri': fields.Url('orders')
}


class Order:
    """
    This contains the methods to add, update and delete an order
    """

    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.status = "Pending"
        self.order_id = order_count

    def __repr__(self):
        return "<Order {}".format(self.order_id)

    def json(self):
        return {
            "order_id": self.order_id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "status": self.status
        }

    def save(self):
        """Creates an order and appends this information to orders dictionary"""
        all_orders[order_count] = {
            "order_id": self.order_id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "status": self.status
        }
        new_order = all_orders[order_count]
        order_count += 1
        return new_order

    @classmethod
    def update(cls, order_id, name, quantity, price, status):
        """Updates the order information"""
        if order_id in all_orders.keys():
            all_orders[order_id] = {
                "order_id": order_id,
                "name": name,
                "quantity": quantity,
                "price": price,
                "status": status
            }
            return all_orders[order_id]
        return {"message": "order does not exist"}

    @staticmethod
    def get_all():
        """Gets all the orders saved"""
        return "The total number of orders are: {}".format(len(all_orders)), all_orders

    @staticmethod
    def get_by_id(order_id):
        """Get a single order by its id"""
        order = [order for order in all_orders if order['order_id'] == order_id]
        if len(order) == 0:
            abort(404, 'Order {} not found!'.format(order_id))
        return order

    @staticmethod
    def delete(order_id):
        """Deletes a single order"""
        order = Order.get_by_id(order_id)
        all_orders.remove(order[0])
        return order
