import os
import json


def get_data():
    data = []
    try:
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates/pages/home.json')) as fh:
            file_data = fh.read()

        data = json.loads(file_data, encoding='utf-8')
    except Exception as e:
        pass
    return data


def get_slideshow():
    return [r'images\home\home1.jpg', r'images\home\home2.jpg', r'images\home\home3.jpg']
