import requests
import logging
import os

# logger:
logger = logging.getLogger('request')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Functions:


def parameter_assembling(access_token, date=None, page=None, sort=None):
    parameter_set = {'access_token': access_token,
                     'date': date,
                     'page': page,
                     'sort': sort}
    return parameter_set


def request(base_url, parameters, header):
    """
    Make get request to url, if the request is successful and page is not empty
    return the json content of the page, None is returned otherwise.
    :param base_url:
    :param parameters:
    :param header:
    :return:
    """
    http_response = requests.get(base_url, params=parameters, headers=header, timeout=None)
    status_code = http_response.status_code
    if status_code == 200:
        logger.info("Access successful, url: {}".format(http_response.url))
        js = http_response.json()
        if len(js) == 0:
            logger.info("Access succeed but page is empty, url: {}".format(http_response.url))
            return None
        else:
            logger.info("Page loaded, url: {}".format(http_response.url))
            return js
    elif status_code == 429:
        logger.info("Reach request rate limit, url: {}".format(http_response.url))
        return None
    elif status_code == 502:
        logger.info("Server offline, url: {}".format(http_response.url))
        return None
    elif status_code == 401:
        logger.info("Unauthorized, access token is invalid, url: {}".format(http_response.url))


def setup_dir(date):
    dir_name = str(date)
    if os.path.exists(dir_name):
        logger.info("Directory for {} is exists.".format(dir_name))
        os.chdir(dir_name)
        return os.getcwd()
    else:
        os.mkdir(dir_name)
        logger.info("Directory for {} is created.".format(dir_name))
        os.chdir(dir_name)
        return os.getcwd()


def download_image(url, shot_id, header):
    file_name = str(shot_id) + url[-4:]
    http_response = requests.get(url, headers=header, timeout=None)
    status_code = http_response.status_code
    if status_code == 200:
        logger.info("Image {} found.".format(shot_id))
        file = open(file_name, 'wb')
        file.write(http_response.content)
        file.close()
        if file.closed:
            logger.info("Image {} saved.".format(shot_id))
        else:
            logger.info("File {} not closed properly".format(shot_id))
    else:
        http_response.raise_for_status()

