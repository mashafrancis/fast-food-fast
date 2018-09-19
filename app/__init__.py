from flask import Flask
from flask_moment import Moment
from flask_cors import CORS

from instance.config import app_config
from swagger_ui.flask_swagger_ui import get_swaggerui_blueprint

moment = Moment()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app_config[config_name].init_app(app)
    CORS(app)

    swagger_url = '/api/v1/docs'
    api_url = 'swagger_doc.yml'

    swaggerui_blueprint = get_swaggerui_blueprint(swagger_url, api_url)

    moment.init_app(app)

    app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)

    from app.api.v1.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1/')

    from app.api.v1.orders import orders as orders_blueprint
    app.register_blueprint(orders_blueprint, url_prefix='/api/v1/')

    return app
