from flask_api import FlaskAPI
from flask_restful import Resource, Api

from app.orders.views import OrderList, Orders
from instance.config import app_config


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    api = Api(app)

    api.add_resource(OrderList, '/v1/orders')
    api.add_resource(Orders, '/v1/orders/<int:order_id>')

    return app
