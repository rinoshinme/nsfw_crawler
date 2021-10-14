"""
BaseNSFWCrawler is an 2-level image crawler.
    Given a page index, with homepage and category, page url is generated. In each 
    page, a set of urls for image series is generated. Each image serie url contains a set of 
    image urls, download each url into a separate folder, and all done.
"""

import requests
from bs4 import BeautifulSoup
import os
from urllib import request
import time


HEADERS = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/2.0.0.11'}


class BaseNSFWCrawler(object):
    def __init__(self):
        pass
    
    def get_page_url(self, page_index):
        raise NotImplementedError
    
    def get_page_info(self, page_url):
        raise NotImplementedError

    def get_set_info(self, set_url):
        raise NotImplementedError
    
    def download_image(self, image_url, image_path):
        try:
            req = request.Request(image_url, headers=HEADERS)
            data = request.urlopen(req).read()
            if len(data) > 0:
                with open(image_path, 'wb') as f:
                    f.write(data)
        except Exception as e:
            print('download error: ' + str(e))
            return
    
    def title_simplify(self, title):
        title = title.replace('?', '').replace(':', '').replace('|', '')
        return title

    def run(self, save_root, start=1, end=-1):
        current = start
        while True:
            print('[Page] {}'.format(current))
            page_url = self.get_page_url(current)
            set_data = self.get_page_info(page_url)
            for info in set_data:
                set_url = info['url']
                title = info['title']
                title = self.title_simplify(title)
                print('[Set] {}'.format(title))
                image_urls = self.get_set_info(set_url)
                for imgurl in image_urls:
                    save_name = os.path.basename(imgurl)
                    save_folder = os.path.join(save_root, title)
                    if not os.path.exists(save_folder):
                        os.makedirs(save_folder)
                    save_path = os.path.join(save_folder, save_name)
                    if not os.path.exists(save_path):
                        print('[Image] {}'.format(imgurl))
                        self.download_image(imgurl, save_path)
                        time.sleep(0.1)
            current += 1
            if end > 0 and current > end:
                break


class MultiProcessWrapper(object):
    """
    TODO: 
    """
    def __init__(self):
        pass
