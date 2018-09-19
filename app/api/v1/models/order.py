from app.data import Database
from app.api.v1.utils import Savable


class Orders(Savable):
    collection = 'orders'

    def __init__(self, order_id, name, quantity, price, date_created, created_by, status):
        self.order_id = order_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.date_created = date_created
        self.created_by = created_by
        self.status = status

    def __repr__(self):
        return f'<Order {self.name}'

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price,
            'date_created': self.date_created,
            'created_by': self.created_by,
            'status': self.status
        }

    def add_order(self):
        """Adds user to the list"""
        order = Orders(self.order_id,
                       self.name,
                       self.quantity,
                       self.price,
                       self.date_created,
                       self.created_by,
                       self.status)
        order.save_order()
        return self.to_dict()

    @staticmethod
    def list_all_orders():
        users = Database.find_all(Orders.collection)
        return users

    @classmethod
    def find_by_id(cls, order_id):
        finder = (lambda x: x['order_id'] == order_id)
        return Database.find_one(Orders.collection, finder)

    @staticmethod
    def delete(order_id):
        finder = (lambda x: x['order_id'] == order_id)
        return Database.remove(Orders.collection, finder)

    @staticmethod
    def delete_all():
        return Database.remove_all(Orders.collection)


