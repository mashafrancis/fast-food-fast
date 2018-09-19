from flask import Blueprint

orders = Blueprint('order', __name__, url_prefix='/api/v1/')

from . import views, errors