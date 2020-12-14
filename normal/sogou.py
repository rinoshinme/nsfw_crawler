import requests
from bs4 import BeautifulSoup
import re
import os
from urllib import request
import time
import socket
import json


headers = {
    'accept': "application/json, text/javascript, */*; q=0.01",
    'x-requested-with': "XMLHttpRequest",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    'cache-control': "no-cache",
    'postman-token': "fab4fce6-bc85-d134-e42e-a73628962c1f"
}


class SogouImageCrawler(object):
    def __init__(self, save_root, mode=0, page_size=48):
        """
        mode:
            0: all sizes
            1: large size
            2: medium size
            3: small size
        """
        self.save_root = save_root
        self.mode = mode
        self.page_size = page_size  # sogou constant
        socket.setdefaulttimeout(5)

    def crawl(self, keyword, num_images=100):
        num_pages = (num_images + self.page_size - 1) // self.page_size
        for i in range(num_pages):
            urls = self.get_urls(keyword, start=i * self.page_size)
            print('next: downloading {} images'.format(len(urls)))
            self.download_urls(keyword, urls)
    
    def crawl_from_file(self, keyword_file, multiprocess=False):
        with open(keyword_file, 'r', encoding='utf-8') as f:
            data = f.read()
            keys = json.loads(data)
        if not multiprocess:
            for key, num in keys.items():
                self.crawl(key, num)
        else:
            pass
    
    def get_urls(self, keyword, start):
        url = 'https://pic.sogou.com/pics?query={}&mode={}&start={}&len={}&reqType=ajax&reqFrom=result&tn=0'.format(keyword, self.mode, start, self.page_size)
        response = requests.get(url, headers=headers)
        html = BeautifulSoup(response.text, features='lxml')
        urls = re.findall("thumbUrl(.*?),", str(html), re.S)
        image_urls = []
        for url in urls:
            url = url[3:-1]
            # print(url)
            image_urls.append(url)
        return image_urls

    def download_urls(self, keyword, urls):
        save_folder = os.path.join(self.save_root, keyword)
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        for img_url in urls:
            print('downloading {}'.format(img_url))
            basename = os.path.basename(img_url)
            if not basename.endswith('.jpg'):
                basename = basename + '.jpg'
            save_path = os.path.join(save_folder, basename)
            if not os.path.exists(save_path):
                try:
                    request.urlretrieve(img_url, save_path)
                except Exception as e:
                    print('download erro: ' + str(e))
            time.sleep(0.05)


if __name__ == "__main__":
    crawler = SogouImageCrawler('./images')
    # crawler.crawl('拉横幅', 1000)
    crawler.crawl_from_file('jobs/street.json', multiprocess=False)
