import datetime

from flask import request, jsonify, Blueprint
from flask.views import MethodView

from app.api.v1.common.decorators import user_required, admin_required
from app.data import Database
from app.api.v1.models.order import Orders
from app.responses import Error, Success, Response

orders = Blueprint('order', __name__)


class OrdersView(MethodView):
    """Contains GET and POST methods"""

    def __init__(self):
        super().__init__()
        self.error = Error()
        self.success = Success()
        self.response = Response()

    @user_required
    def get(self, user_id):
        """Endpoint for fetching all orders."""
        results = []
        all_orders = Orders.list_all_orders()
        if all_orders:
            for order in all_orders:
                obj = self.response.define_orders(order)
                results.append(obj)
            return self.success.complete_request(results)
        else:
            return self.error.not_found('Sorry, No orders for you!')

    @user_required
    def post(self, user_id):
        """Endpoint for adding a new order."""
        data = request.get_json(force=True)
        order_id = Database.order_count() + 1
        name = data['name']
        quantity = data['quantity']
        price = data['price']
        date_created = datetime.datetime.now()
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
        return jsonify({'message': 'Order has been added successfully.',
                        'Order No {}'.format(order_id): created_order}), 201

    @user_required
    def delete(self, user_id):
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

    @user_required
    def get(self, order_id, user_id):
        """Endpoint for fetching a particular order."""
        order = Orders.find_by_id(order_id)
        if not order:
            return self.error.not_found("Sorry, Order No {} does't exist!".format(order_id))
        return self.success.complete_request(order)

    @user_required
    def put(self, order_id, user_id):
        """Endpoint for updating a particular order."""
        order = Orders.find_by_id(order_id)
        data = request.get_json(force=True)
        if not order:
            return self.error.not_found("Sorry, Order No {} doesn't exist yet! Create one.".format(order_id))
        else:
            order[0]['name'] = data['name']
            order[0]['quantity'] = data['quantity']
            order[0]['price'] = data['price']
            return jsonify({'order': order[0]}), 200

    @admin_required
    def patch(self, order_id, user_id):
        """Endpoint for updating the status."""
        order = Orders.find_by_id(order_id)
        data = request.get_json(force=True)
        if not order:
            return self.error.not_found("Sorry, Order No {} doesn't exist yet! Create one.".format(order_id))
        else:
            order[0]['status'] = data['status']
            return jsonify({'order': order[0]}), 200

    @user_required
    def delete(self, order_id, user_id):
        """Endpoint for deleting a particular order."""
        order = Orders.find_by_id(order_id)
        if order:
            Orders.delete(order_id)
            response = "Order No {} has been deleted!".format(order_id)
            return self.success.complete_request(response)
        else:
            return self.error.not_found("Order No {} does not exist!".format(order_id))


# Define API resource
orders_view = OrdersView.as_view('orders_view')
order_view = OrderView.as_view('order_view')

orders.add_url_rule('orders',
                    view_func=orders_view,
                    methods=['POST', 'GET', 'DELETE'])

orders.add_url_rule('orders/<int:order_id>',
                    view_func=order_view,
                    methods=['PUT', 'GET', 'PATCH', 'DELETE'])
