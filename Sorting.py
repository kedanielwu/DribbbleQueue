class SourceException(Exception):
    pass


class Sorting:

    def __init__(self, response, source='like', tags=None, authors=None):
        self.response_set = response
        self.result_set = []
        self.raw_list = []
        self.tags = tags
        self.author_set = authors

        # by default, sort by like
        self.source = source

        source_set = self.extract_source_by_tag(self.source)
        self.unpack(source_set)
        self.result_set = self.sort(self.raw_list)

    def extract_source_by_tag(self, source='like'):
        source_set = {}
        for key in self.response_set.keys():
            flag = False
            tags = self.response_set[key].get_tags()
            for tag in tags:
                if tag in self.tags:
                    flag = True
            if flag:
                count = self.response_set[key].get_popularity()[source]
                source_set[key] = count

        return source_set

    def extract_source(self, source='like'):
        """
        source must be view, like, or comment
        :param source:
        :return:
        """
        source_set = {}
        for key in self.response_set.keys():
            count = self.response_set[key].get_popularity()[source]
            source_set[key] = count
        return source_set

    def unpack(self, source_set):
        for key in source_set:
            self.raw_list.append((key, source_set[key]))

    def sort(self, raw_list):
        """
        Sort list using merge sort
        :param raw_list:
        :return:
        """
        if len(raw_list) <= 1:
            return raw_list

        left = []
        right = []

        for i in range(len(raw_list)):
            if i % 2 == 0:
                right.append(raw_list[i])
            else:
                left.append(raw_list[i])

        left = self.sort(left)
        right = self.sort(right)

        return self._merge(left, right)

    def _merge(self, left, right):

        result = []

        while len(left) != 0 and len(right) != 0:
            if left[0][1] <= right[0][1]:
                result.append(left[0])
                left.pop(0)
            else:
                result.append(right[0])
                right.pop(0)

        while len(left) != 0:
            result.append(left[0])
            left.pop(0)

        while len(right) != 0:
            result.append(right[0])
            right.pop(0)

        return result

    # Pubic API

    def get_result(self):
        return self.result_set[-10:]

    def set_source(self, source):
        if source != 'like' or source != 'view' or source != 'comment':
            raise SourceException('Source entered is invalid')
        else:
            self.source = source
