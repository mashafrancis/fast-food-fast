from flasgger import Swagger
from flask import Flask

from instance.config import app_config
from .template import template


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    Swagger(app, template=template)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .orders import orders as orders_blueprint
    app.register_blueprint(orders_blueprint)

    return app
