from flask import Flask
from flask_restful import Resource, Api

from app.orders.views import Orders
from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    api = Api(app)

    api.add_resource(Orders, '/v1/orders')

    return app
