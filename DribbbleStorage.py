import datetime
from Shot import *
from Author import *
from Sorting import *
import os
import logging
from queue import Queue
from Download import *
from threading import Thread
import requests


# Global Variables:
SHOTS_API_URL = 'https://api.dribbble.com/v1/shots'
ACCESS_TOKEN = ''
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
           'Accept-Encoding': 'gzip'}


class RequestsWorker(Thread):

    def __init__(self, queue, storage):
        Thread.__init__(self)
        self.storage = storage
        self.queue = queue
        self.logger = logging.getLogger('RequestsWorker')
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def run(self):
        while True:
            parameter_set = self.queue.get()
            try:
                js = request(SHOTS_API_URL, parameter_set, HEADERS)
                if js is not None:
                    self.storage.append(js)
                self.queue.task_done()
            except requests.HTTPError as e:
                self.logger.info("Exception caught, {}".format(e))


class DownloadWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.logger = logging.getLogger("DownloadWorker")

    def run(self):
        while True:
            try:
                content = self.queue.get()
                download_image(content[1], content[0], HEADERS)
                self.queue.task_done()
            except requests.HTTPError as e:
                self.logger.info("Exception caught, {}".format(e))


class Factory:

    def __init__(self):
        # work flow variable:
        self.work_queue = Queue()
        self.image_queue = Queue()
        self.json_pool = []

        # storage variable:
        self.shots = {}
        self.top_10 = []

        # environment variable:
        self.date = '2016-08-02'
        self.source = 'like'
        self.tags = []

        # logger:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            filename='log.log',
                            filemode='w')
        self.logger = logging.getLogger('request')

        # setup:
        self.path = setup_dir(self.date)
        self.fill_parameter_pool(50)
        self.create_request_worker(8)
        self.work_queue.join()

        for i in range(len(self.json_pool)):
            self.construct(self.json_pool[i])

    def extracting(self):
        if self.tags:
            name = str(self.tags)
        else:
            name = 'top 10'
        os.mkdir(name)
        os.chdir(name)
        self.extract_top10(tags=self.tags, source=self.source)
        self.fill_image_pool(self.top_10)
        self.create_download_worker(4)
        self.image_queue.join()

    def download_all(self):
        os.mkdir("All")
        os.chdir("All")
        self.fill_image_pool(self.shots)
        self.create_download_worker(4)
        self.image_queue.join()

    # Threading Setup

    def fill_parameter_pool(self, size):
        for i in range(1, size + 1):
            ps = parameter_assembling(ACCESS_TOKEN, date=self.date, page=i)
            self.work_queue.put(ps)
            self.logger.info("Enqueue page {}.".format(i))

    def fill_image_pool(self, source):
        for shot in source:
            image_url = self.shots[shot].get_image_url()
            self.image_queue.put((shot, image_url))
            self.logger.info("Enqueue image for shot_id {}.".format(shot))

    def create_request_worker(self, size):
        for i in range(size):
            worker = RequestsWorker(self.work_queue, self.json_pool)
            self.logger.info("Request worker {} is instantiated.".format(i + 1))
            worker.daemon = True
            worker.start()

    def create_download_worker(self, size):
        for i in range(size):
            worker = DownloadWorker(self.image_queue)
            self.logger.info("Download worker {} is instantiated".format(i + 1))
            worker.daemon = True
            worker.start()

    # Data Analysis

    def construct(self, json_file):
        total = len(json_file)
        for i in range(total):
            # Source collecting
            shot_id = json_file[i]['id']
            user_id = json_file[i]['user']['id']
            shot_image_url = json_file[i]['images']['normal']
            # if shot_image_url is None:
            #     shot_image_url = json_file[i]['images']['normal']
            avatar_url = json_file[i]['user']['avatar_url']
            shot_description = json_file[i]['description']
            user_name = json_file[i]['user']['name']
            view = json_file[i]['views_count']
            like = json_file[i]['likes_count']
            comment = json_file[i]['comments_count']
            tags = json_file[i]['tags']

            # animated flag
            flag = json_file[i]['animated']

            # Record Building
            new_shot = Shot(shot_id)
            new_shot.load_description(shot_description)
            new_shot.load_image_url(shot_image_url)
            new_shot.load_popularity(view, like, comment)
            new_shot.load_tags(tags)

            new_author = Author(user_id)
            new_author.load_avatar_url(avatar_url)
            new_author.load_name(user_name)

            new_shot.add_author(new_author)

            if flag is False:
                self.shots[shot_id] = new_shot
                self.logger.info("Shot id: {} is decoded.".format(shot_id))
            else:
                self.logger.info("Shot id: {} is omitted.".format(shot_id))

    def extract_top10(self, tags=[], source=None):
        sort = Sorting(self.shots, tags=tags, source=source)
        listing = sort.get_result()
        for tup in listing:
            self.top_10.append(tup[0])
        self.logger.info("Top 10 is extracted.")

    # Public setting API

    def add_tag(self, new_tag):
        self.tags.append(new_tag)

    def add_tag_set(self, tag_set):
        self.tags.extend(tag_set)

    def set_preference(self, source):
        self.source = source

    def report_top(self):
        for shot in self.top_10:
            print("shot id: {}, likes: {}".format(shot, self.shots[shot].get_popularity()['like']))

# if __name__ == '__main__':
#     print("====== Welcome to Dribbble Daily Top 10 ======")
#     raw_in = input("Enter something you are interested in, separated by comma: ")
#     raw_tags = raw_in.split(',')
#     tags = []
#     for tag in raw_tags:
#         tags.append(tag.strip())
#     print("====== Tags received, Generating Top 10 for you ======")
#     time.sleep(1)
#     ds = Factory()
#     ds.add_tag_set(tags)
#     ds.extracting()
#     time.sleep(1)
#     print("====== Work Done! You will see the result below, all images are downloaded ======")
#     ds.report_top()

