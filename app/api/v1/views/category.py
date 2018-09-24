from flask import request, jsonify, Blueprint
from flask.views import MethodView

import app.responses as CategoryError

from app.api.v1.common.decorators import user_required
from app.api.v1.models.category import Category
from app.data import Database
from app.responses import Response

category = Blueprint('category', __name__)


class CategoryView(MethodView):
    """Contains GET and POST methods"""

    @user_required
    def post(self, user_id):
        """Endpoint for adding a new order."""
        data = request.get_json(force=True)
        name = data['name']
        description = data['description']

        categories = Category(name=name,
                              description=description)
        categories.save_category()
        return Response.create_resource('A new category has been added successfully.')

    @user_required
    def get(self, user_id):
        """Endpoint for fetching all orders."""
        results = []
        all_categories = Category.list_all_categories()
        try:
            if all_categories:
                for category in all_categories:
                    obj = Response.define_category(category)
                    results.append(obj)
                return Response.complete_request(results)
            else:
                raise CategoryError.NotFound('Sorry, No Category found! Create one.')
        except CategoryError.NotFound as e:
            return e.message

    @user_required
    def delete(self, user_id):
        """Endpoint for deleting all orders."""
        try:
            if Database.category_count() == 0:
                raise CategoryError.NotFound('There is no category here!')
            else:
                Category.delete_all()
                return Response.complete_request('All categories have been successfully deleted!')
        except CategoryError.NotFound as e:
            return e.message


# Define API resource
category_view = CategoryView.as_view('category_view')

category.add_url_rule('category',
                      view_func=category_view,
                      methods=['POST', 'GET', 'DELETE'])
