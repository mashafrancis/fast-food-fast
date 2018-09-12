class Database:
    content = {'users': [],
               'orders': []}

    @classmethod
    def insert(cls, data):
        cls.content['users'].append(data)

    @classmethod
    def remove(cls, finder):    # lambda x: x['username'] != 'francis'
        cls.content['users'] = [user for user in cls.content['users'] if not finder(user)]

    @classmethod
    def find(cls, finder):  # lambda x: x['username'] == 'francis'
        return [user for user in cls.content['users'] if finder(user)]

    @classmethod
    def get_all_users(cls):
        return cls.content['users']

    @classmethod
    def user_count(cls):
        return len(cls.content['users'])
