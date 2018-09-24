import datetime

from flask import request, jsonify, Blueprint
from flask.views import MethodView

import app.responses as OrderError

from app.api.v1.common.decorators import user_required
from app.data import Database
from app.api.v1.models.order import Orders
from app.responses import Response

orders = Blueprint('order', __name__)


class OrdersView(MethodView):
    """Contains GET and POST methods"""

    @user_required
    def get(self, user_id):
        """Endpoint for fetching all orders."""
        results = []
        all_orders = Orders.list_all_orders()
        try:
            if all_orders:
                for order in all_orders:
                    obj = Response.define_orders(order)
                    results.append(obj)
                return Response.complete_request(results)
            else:
                raise OrderError.NotFound('Sorry, No orders for you!')
        except OrderError.NotFound as e:
            return e.message

    @user_required
    def post(self, user_id):
        """Endpoint for adding a new order."""
        data = request.get_json(force=True)
        name = data['name']
        quantity = data['quantity']
        price = data['price']
        created_by = data['created_by']

        order = Orders(name=name,
                       quantity=quantity,
                       price=price,
                       created_by=created_by)
        order.add_order()
        return Response.create_resource('Order has been added successfully.')

    @user_required
    def delete(self, user_id):
        """Endpoint for deleting all orders."""
        try:
            if Database.order_count() == 0:
                raise OrderError.NotFound('No orders available!')
            else:
                Orders.delete_all()
                return Response.complete_request('All orders have been successfully deleted!')
        except OrderError.NotFound as e:
            return e.message


class OrderView(MethodView):
    """Contains GET, PUT and DELETE methods for manipulating a single order"""

    @user_required
    def get(self, order_id, user_id):
        """Endpoint for fetching a particular order."""
        try:
            order = Orders.find_by_id(order_id)
            if not order:
                raise OrderError.NotFound("Sorry, Order No {} does't exist!".format(order_id))
            return Response.complete_request(order)
        except OrderError.NotFound as e:
            return e.message

    @user_required
    def put(self, order_id, user_id):
        """Endpoint for updating a particular order."""
        order = Orders.find_by_id(order_id)
        data = request.get_json(force=True)
        try:
            if not order:
                raise OrderError.NotFound("Sorry, Order No {} doesn't exist yet! Create one.".format(order_id))
            else:
                order[0]['name'] = data['name']
                order[0]['quantity'] = data['quantity']
                order[0]['price'] = data['price']
                return jsonify({'order': order[0]}), 200
        except OrderError.NotFound as e:
            return e.message

    @user_required
    def patch(self, order_id, user_id):
        """Endpoint for updating the status."""
        order = Orders.find_by_id(order_id)
        data = request.get_json(force=True)
        try:
            if not order:
                raise OrderError.NotFound("Sorry, Order No {} doesn't exist yet! Create one.".format(order_id))
            else:
                order[0]['status'] = data['status']
                return jsonify({'order': order[0]}), 200
        except OrderError.NotFound as e:
            return e.message

    @user_required
    def delete(self, order_id, user_id):
        """Endpoint for deleting a particular order."""
        order = Orders.find_by_id(order_id)
        try:
            if order:
                Orders.delete(order_id)
                response = "Order No {} has been deleted!".format(order_id)
                return Response.complete_request(response)
            else:
                raise OrderError.NotFound("Order No {} does not exist!".format(order_id))
        except OrderError.NotFound as e:
            return e.message


# Define API resource
orders_view = OrdersView.as_view('orders_view')
order_view = OrderView.as_view('order_view')

orders.add_url_rule('orders',
                    view_func=orders_view,
                    methods=['POST', 'GET', 'DELETE'])

orders.add_url_rule('orders/<int:order_id>',
                    view_func=order_view,
                    methods=['PUT', 'GET', 'PATCH', 'DELETE'])
