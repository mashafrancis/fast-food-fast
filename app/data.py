class Database:
    content = {'users': [],
               'orders': [],
               'blacklist': [],
               'roles': [],
               'category': []}

    @classmethod
    def insert(cls, collection, data):
        cls.content[collection].append(data)

    @classmethod
    def remove_all(cls, collection):
        cls.content[collection].clear()

    @classmethod
    def remove(cls, collection, finder):    # lambda x: x['username'] != 'francis'
        cls.content[collection] = [x for x in cls.content[collection] if not finder(x)]

    @classmethod
    def find_one(cls, collection, finder):  # lambda x: x['username'] == 'francis'
        return [x for x in cls.content[collection] if finder(x)]

    @classmethod
    def find_all(cls, collection):
        return cls.content[collection]

    @classmethod
    def user_count(cls):
        return len(cls.content['users'])

    @classmethod
    def order_count(cls):
        return len(cls.content['orders'])
