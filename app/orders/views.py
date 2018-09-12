from flask import abort, request
from flask.views import MethodView

from app.database import Database
from app.models import Orders
from app.responses.responses import Error, Success, Response
from . import orders


class OrdersView(MethodView):
    """Contains GET and POST methods"""

    def __init__(self):
        super().__init__()
        self.error = Error()
        self.success = Success()
        self.response = Response()

    def get(self):
        results = []
        all_orders = Orders.list_all_orders()
        if all_orders:
            for order in all_orders:
                obj = self.response.orders(order)
                results.append(obj)
            return self.success.complete_request(results)
        else:
            return self.error.not_found('No orders found!')

    def post(self):
        data = request.get_json(force=True)
        order_id = Database.order_count() + 1
        name = data['name']
        quantity = data['quantity']
        price = data['price']
        date_created = 'now'
        created_by = data['created_by']
        status = 'Pending'

        order = Orders(order_id=order_id,
                       name=name,
                       quantity=quantity,
                       price=price,
                       date_created=date_created,
                       created_by=created_by,
                       status=status)
        order.add_order()
        return self.success.create_resource('Order has been created!')

    @staticmethod
    def delete():
        pass


class OrderView(OrdersView):
    """Contains GET, PUT and DELETE methods for manipulating a single ride"""

    def get(self, order_id):
        pass

    def put(self, order_id):
        pass

    def delete(self, order_id):
        pass


# Define API resource
orders_view = OrdersView.as_view('orders_view')
order_view = OrderView.as_view('order_view')

orders.add_url_rule('/v1/orders',
                    view_func=orders_view,
                    methods=['POST', 'GET', 'DELETE'])

orders.add_url_rule('/v1/orders/<int:order_id>',
                    view_func=order_view,
                    methods=['POST', 'PUT', 'GET', 'DELETE'])
