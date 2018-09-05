"""
Handles data storage for all orders and users
"""
from flask import make_response, jsonify

all_orders = {}
order_count = 1


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
        global all_orders
        global order_count

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
        return all_orders

    @staticmethod
    def get_by_id(order_id):
        """Get a single order by its id"""
        return all_orders[order_id]

    @staticmethod
    def delete(order_id):
        """Deletes a single order"""
        try:
            del all_orders[order_id]
            return make_response(jsonify({"message": "order successfully deleted"}), 200)
        except KeyError:
            return make_response(jsonify({"message": "order does not exist"}), 404)
