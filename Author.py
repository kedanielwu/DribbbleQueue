class Author:

    def __init__(self, user_id):
        self.user_id = user_id
        self.name = ""
        self.avatar_url = ""
        self.avatar = ""

    def load_name(self, name):
        self.name = name

    def load_avatar_url(self, url):
        self.avatar_url = url

    def load_avatar(self, content):
        self.avatar = content

    # Public API

    def get_name(self):
        return self.name

    def get_avatar_url(self):
        return self.avatar_url

    def get_avatar(self):
        return self.avatar
