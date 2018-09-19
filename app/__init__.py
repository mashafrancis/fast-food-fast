from flasgger import Swagger
from flask import Flask
from flask_moment import Moment
from flask_cors import CORS

from app.models import User
from instance.config import app_config
from .template import template

moment = Moment()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app_config[config_name].init_app(app)
    CORS(app)

    Swagger(app, template=template)
    moment.init_app(app)

    from app.api.v1.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.api.v1.orders import orders as orders_blueprint
    app.register_blueprint(orders_blueprint)

    return app
