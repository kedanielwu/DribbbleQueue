class Shot:

    def __init__(self, shot_id):
        self.shot_id = shot_id
        self.image_url = ""
        self.image = ""
        self.description = ""
        self.author = ""
        self.popularity = {'view': 0, 'like': 0, 'comment': 0}
        self.tags = []

    def load_tags(self, tag):
        self.tags = tag

    def load_image_url(self, url):
        self.image_url = url

    def load_description(self, content):
        self.description = content

    def add_author(self, author):
        self.author = author

    def load_image(self, content):
        self.image = content

    def load_author_avatar(self, content):
        self.author.load_avatar(content)

    def load_popularity(self, view, like, comment):
        self.popularity['view'] = view
        self.popularity['like'] = like
        self.popularity['comment'] = comment

    # Public API

    def get_popularity(self):
        return self.popularity

    def get_image_url(self):
        return self.image_url

    def get_description(self):
        return self.description

    def get_author_name(self):
        return self.author.get_name()

    def get_author_avatar_url(self):
        return self.author.get_avatar_url()

    def get_image(self):
        return self.image

    def get_author_avatar(self):
        return self.author.get_avatar()

    def get_tags(self):
        return self.tags

    def get_json(self):
        return {'shot_id': self.shot_id,
                'description': self.get_description(),
                'view': self.get_popularity()['view'],
                'like': self.get_popularity()['like'],
                'comment': self.get_popularity()['comment'],
                'author': self.get_author_name(),
                'tags': self.get_tags()}
