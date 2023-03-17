import os
import requests
from urllib import request
from bs4 import BeautifulSoup
import random
import time
from easydict import EasyDict


category2index = {
    'yazhou': 17,
    'oumei': 18
}


def get_configs():
    configs = EasyDict()
    configs.category = 'yazhou'
    configs.start_page = 1
    configs.stop_page = 10
    configs.save_root = '../../data/dy47'
    return configs


HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36' }


class Webcrawler(object):
    def __init__(self, configs):
        self.homepage = 'https://47dy.cc'
        self.configs = configs
        self.category = configs.category
        self.start_page = configs.start_page
        self.stop_page = configs.stop_page
        self.save_root = os.path.join(configs.save_root, self.category)

    def run(self):
        for i in range(self.start_page, self.stop_page):
            page_url = self.get_page_url(self.category, i)
            # get page source
            response = requests.get(page_url, headers=HEADERS)
            time.sleep(0.2)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, features='lxml')
            container = soup.find(attrs={'class': 'stui-vodlist__media active col-pd clearfix'})
            print(container)
            print('-----------')
            for item in container.find_all(attrs={'class': 'top-line-dot'}):
                item = item.find(attrs={'class': 'title'})
                url = item.a['href']
                url = self.homepage + url
                title = item.text
                print(url)
                print(title)

                image_urls = self.get_set_info(url)
                print(image_urls)
                # # download set
                # print(f'[SET] {title}')
                # set_folder = os.path.join(self.save_root, self.safe_name(title))
                # if not os.path.exists(set_folder):
                #     os.makedirs(set_folder)
                # for url in image_urls:
                #     filename = os.path.basename(url)
                #     print(f'[IMAGE]{url}')
                #     image_path = os.path.join(set_folder, filename)
                #     self.http_download(url, image_path)
            break
    
    def get_set_info(self, set_url):
        """
        get image urls from the set
        """
        response = requests.get(set_url, headers=HEADERS)
        time.sleep(0.2)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, features='lxml')
        print(soup)

        container = soup.find(attrs={'class': 'article_content'})
        urls = []
        for img in container.find_all('img'):
            img_url = img['src']
            urls.append(img_url)
        return urls

    def get_page_url(self, category, pn):
        index = category2index[category]
        return f'https://47dy.cc/pic_type_{index}_{pn}.htm'

    def http_download(self, url, save_path):
        if os.path.exists(save_path):
            return
        try:
            req = request.Request(url, headers=HEADERS)
            data = request.urlopen(req).read()
            if len(data) == 0:
                return
            with open(save_path, 'wb') as f:
                f.write(data)
            time.sleep(0.2)
        except Exception as e:
            print(str(e))
    
    def safe_name(self, name):
        chars = ['?', '|', '!', '']
        for c in chars:
            name = name.replace(c, '')
        return name


if __name__ == '__main__':
    configs = get_configs()
    downloader = Webcrawler(configs)
    downloader.run()
