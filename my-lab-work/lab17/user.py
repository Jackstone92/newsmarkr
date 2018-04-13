class User:

    def __init__(self, user_id):
        self.user_id = user_id

    @property
    def username(self):
        return self.username

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
       return self.user_id

    def __repr__(self):
        return 'user_id {}'.format(self.user_id)
