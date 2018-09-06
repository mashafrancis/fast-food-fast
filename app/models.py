"""
Handles data storage for all orders and users
"""
from flask_restful import fields, marshal

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


class Order(object):
    """
    This contains the methods to add, update and delete an order
    """
    def save(self):
        """Creates an order and appends this information to orders dictionary"""
        pass

    @classmethod
    def update(cls, order_id, name, quantity, price, status):
        """Updates the order information"""
        pass

    @staticmethod
    def get_all():
        """Gets all the orders saved"""
        return [marshal(order, order_fields) for order in all_orders]

    @staticmethod
    def get_by_id(order_id):
        """Get a single order by its id"""
        return [order for order in all_orders if order['order_id'] == order_id]

    @staticmethod
    def delete(order_id):
        """Deletes a single order"""
        order = Order.get_by_id(order_id)
        all_orders.remove(order[0])
        return order
