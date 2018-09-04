"""
Handles data storage for all orders and users
"""
ORDERS = []


class Order:
    """
    This contains the methods to add, update and delete an order
    """

    def __init__(self, name, quantity, price, status="pending"):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.status = status
        self._id = len(ORDERS)+1

    def __repr__(self):
        return "<Order {}".format(self._id)

    def json(self):
        return {
            "id": self._id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "status": self.status
        }

    def save(self):
        """Creates an order and appends this information to orders dictionary"""
        global ORDERS

        ORDERS[self._id] = {
            "id": self._id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "status": self.status
        }
        new_order = ORDERS[self._id]
        ORDERS.append(new_order)

    def update(self):
        """Updates the order information"""
        pass

    def get_all(self):
        """Gets all the orders saved"""
        pass

    def get_by_id(self):
        """Get a single order by its id"""
        next(filter(lambda x: x[self._id] == self._id, ORDERS), None)

    def delete(self):
        global ORDERS
        ORDERS.pop(self._id)
