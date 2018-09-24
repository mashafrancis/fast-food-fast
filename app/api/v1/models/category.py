from datetime import datetime

from app.data import Database
from app.api.v1.common.utils import Savable


class Category(Savable):
    collection = 'category'

    def __init__(self, name, description):
        self.category_id = Database.order_count() + 1
        self.name = name
        self.description = description
        self.date_created = datetime.now()

    def __repr__(self):
        return f'<Category {self.name}'

    def to_dict(self):
        return {
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'date_created': self.date_created
        }

    def add_category(self):
        """Adds user to the list"""
        order = Category(self.name,
                         self.description)
        order.save_category()
        return self.to_dict()

    @staticmethod
    def list_all_categories():
        users = Database.find_all(Category.collection)
        return users

    @classmethod
    def find_by_id(cls, category_id):
        finder = (lambda x: x['category_id'] == category_id)
        return Database.find_one(Category.collection, finder)

    @staticmethod
    def delete(category_id):
        finder = (lambda x: x['category_id'] == category_id)
        return Database.remove(Category.collection, finder)

    @staticmethod
    def delete_all():
        return Database.remove_all(Category.collection)
