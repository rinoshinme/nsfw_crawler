import requests
from bs4 import BeautifulSoup
import os
from urllib import request
import time
import random


headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/2.0.0.11'}


class NewlyNet(object):
    def __init__(self, save_root, category='meinvtupian'):
        self.homepage = 'http://a.newlynet.com'
        self.category = category
        self.save_root = save_root
        self.res_encoding = 'gb2312'
    
    def get_page_info(self, page_index):
        if page_index == 1:
            page_url = '{}/{}/'.format(self.homepage, self.category)
        else:
            page_url = '{}/{}/page_{}.html'.format(self.homepage, self.category, page_index)

        data = []
        try:
            response = requests.get(page_url, headers=headers)
            response.encoding = self.res_encoding
            soup = BeautifulSoup(response.text, features='lxml')
            items = soup.find_all(attrs={'class': 'neiRon2'})
            for item in items:
                url = item.a['href']
                title = item.a['title']
                url = self.homepage + url
                data.append({
                    'url': url,
                    'title': title
                    })
        except Exception as e:
            print('error: ' + str(e))
        return data
    
    def get_set_info(self, set_url):
        """
        # 1 page for each image instead of putting all images in 1 page.
        1. get image pages from first page
        2. get image urls from image pages.
        """
        urls = []
        try:
            response = requests.get(set_url, headers=headers)
            response.encoding = self.res_encoding
            soup = BeautifulSoup(response.text, features='lxml')
            container = soup.find(attrs={'class': 'pageInsd2'}).p
            for d in container.find_all('a'):
                urls.append(self.homepage + d['href'])
            
        except Exception as e:
            print('error: ' + str(e))
        return urls
    
    def get_image_from_url(self, image_url):
        try:
            response = requests.get(image_url, headers=headers)
            response.encoding = self.res_encoding
            soup = BeautifulSoup(response.text, features='lxml')
            container = soup.find(attrs={'class': 'cont'})

            img = container.find('img')
            url = img['data-original']
            return url
        except Exception as e:
            print('error: ' + str(e))
        return None

    def run(self, shuffle=True):
        for i in range(4, 100):
            print('downloading page {}'.format(i))
            data = self.get_page_info(i)
            if shuffle:
                random.shuffle(data)
            for d in data:
                set_url = d['url']
                title = d['title']
                title = title.replace('?', '')
                set_folder = os.path.join(self.save_root, title)
                if not os.path.exists(set_folder):
                    os.makedirs(set_folder)
                print('downloading set {}'.format(title))
                image_page_urls = self.get_set_info(set_url)
                for url in image_page_urls:
                    image_url = self.get_image_from_url(url)
                    if image_url is None:
                        continue
                    # download image
                    image_name = image_url.split('/')[-1]
                    image_path = os.path.join(set_folder, image_name)
                    if os.path.exists(image_path):
                        continue
                    print('[IMAGE][{}]downloading {}'.format(time.asctime(), image_url))
                    self.download_image(image_url, image_path)
    

    def download_image(self, image_url, image_path):
        try:
            req = request.Request(image_url, headers=headers)
            data = request.urlopen(req).read()
        except Exception as e:
            print('download error: ' + str(e))
            return 
        # save data
        if len(data) > 0:
            with open(image_path, 'wb') as f:
                f.write(data)


if __name__ == '__main__':
    download_dir = r'F:/Data/crawler_data/newly'
    crawler = NewlyNet(download_dir)
    crawler.run()
