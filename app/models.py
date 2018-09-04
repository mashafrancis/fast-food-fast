"""
Handles data storage for all orders and users
"""
ORDERS = {}


class Order:
    """
    This contains the methods to add, update and delete an order
    """

    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.status = "Pending"
        self.order_id = len(ORDERS)+1

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
        global ORDERS

        ORDERS[self.order_id] = {
            "order_id": self.order_id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "status": self.status
        }
        new_order = ORDERS[self.order_id]
        return new_order

    def update(self):
        """Updates the order information"""
        pass

    @staticmethod
    def get_all():
        """Gets all the orders saved"""
        return ORDERS

    def get_by_id(self):
        """Get a single order by its id"""
        next(filter(lambda x: x[self.order_id] == self.order_id, ORDERS), None)

    def delete(self):
        global ORDERS
        ORDERS.pop(self.order_id)
