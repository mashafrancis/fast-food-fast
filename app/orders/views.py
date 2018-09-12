from flask import abort, request, jsonify
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
        """Endpoint for fetching all orders."""
        results = []
        all_orders = Orders.list_all_orders()
        if all_orders:
            for order in all_orders:
                obj = self.response.define_orders(order)
                results.append(obj)
            return self.success.complete_request(results)
        else:
            return self.error.not_found('No orders found!')

    def post(self):
        """Endpoint for adding a new order."""
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
        created_order = Orders.find_by_id(order_id)
        return jsonify({'message': 'Order has been added!', 'Order No {}'.format(order_id): created_order}), 201

    def delete(self):
        """Endpoint for deleting all orders."""
        if Database.order_count() == 0:
            return self.error.not_found('No orders available!')
        else:
            Orders.delete_all()
            return self.success.complete_request('All orders have been successfully deleted!')


class OrderView(MethodView):
    """Contains GET, PUT and DELETE methods for manipulating a single ride"""
    def __init__(self):
        super().__init__()
        self.error = Error()
        self.success = Success()
        self.response = Response()

    def get(self, order_id):
        """Endpoint for fetching a particular order."""
        order = Orders.find_by_id(order_id)
        if not order:
            return self.error.not_found("Order not found!")
        return self.success.complete_request(order)

    def put(self, order_id):
        """Endpoint for updating a particular order."""
        order = Orders.find_by_id(order_id)
        data = request.get_json(force=True)
        if not order:
            return self.error.not_found("Order does not exist!")
        else:
            order[0]['name'] = data['name']
            order[0]['quantity'] = data['quantity']
            order[0]['price'] = data['price']
            order[0]['status'] = data['status']
            return jsonify({'order': order[0]}), 200

    def patch(self):
        """Endpoint for updating a single value in an order."""
        pass

    def delete(self, order_id):
        """Endpoint for deleting a particular order."""
        order = Orders.find_by_id(order_id)
        if order:
            Orders.delete(order_id)
            response = "Order has been deleted!"
            return self.success.complete_request(response)
        else:
            return self.error.not_found("Order does not exist!")


# Define API resource
orders_view = OrdersView.as_view('orders_view')
order_view = OrderView.as_view('order_view')

orders.add_url_rule('/v1/orders',
                    view_func=orders_view,
                    methods=['POST', 'GET', 'DELETE'])

orders.add_url_rule('/v1/orders/<int:order_id>',
                    view_func=order_view,
                    methods=['POST', 'PUT', 'GET', 'DELETE'])
