import os
import requests
from urllib import request
from bs4 import BeautifulSoup
import json
import wget
import random

from .base import BaseNSFWCrawler, HEADERS


class Hu4Image(BaseNSFWCrawler):
    CATEGORIES = []

    def __init__(self, category):
        self.category = category
        self.homepage = 'https://www.4huxx339.com/'
        self.res_encoding = 'utf-8'
    
    def get_page_url(self, page_index):
        if page_index == 1:
            page_url = '{}/pic/{}'.format(self.homepage, self.category)
        else:
            page_url = '{}/pic/{}/index_{}.html'.format(self.homepage, self.category, page_index)
        return page_url
    
    def get_page_info(self, page_url):
        data = []
        try:
            response = requests.get(page_url, headers=HEADERS)
            response.encoding = self.res_encoding
            soup = BeautifulSoup(response.text, features='lxml')
            items = soup.find_all('dl')
            for item in items:
                try:
                    item = item.dd.a
                    title = item['title']
                    url = item['href']
                    url = self.homepage + url
                    data.append({
                        'url': url, 
                        'title': title
                    })
                except Exception as ee:
                    print('error: ' + str(ee))
                    
        except Exception as e:
            print('error: ' + str(e))
        
        return data
    
    def get_set_info(self, set_url):
        image_urls = []
        try:
            response = requests.get(set_url, headers=HEADERS)
            response.encoding = self.res_encoding
            soup = BeautifulSoup(response.text, features='lxml')
            container = soup.find(attrs={'class': 'pic'})

            for d in container.find_all('img'):
                image_urls.append(d['src'])

        except Exception as e:
            print('error: ' + str(e))
        
        return image_urls


class Hu4Video(object):
    HU4_VIDEO_CATEGORIES = {
        'video': ['zipai', 'fuqi', 'kaifang', 'jingpin', 
                  'twmn', 'krzb', 'dongman', 'sanji'],
        'av': ['nxx', 'bdyjy', 'stym', 'qbyc', 
               'cjk', 'ssyy', 'thy', 'jzmb'],
        'movie': ['wuma', 'sm', 'gaoqing', 'shunv', 
                  'meiyan', 'siwa', 'youma', 'oumei'],
    }
    def __init__(self, category_major, category_minor, save_path='4hulinks.json'):
        self.category_major = category_major
        self.category_minor = category_minor
        self.homepage = 'https://www.4huxx339.com/'
        self.res_encoding = 'utf-8'
        self.save_path = save_path
    
    def load_links(self):
        if not os.path.exists(self.save_path):
            return {}
        with open(self.save_path, 'r', encoding='utf-8') as f:
            database = json.loads(f.read())
        return database
    
    def save_links(self, database):
        with open(self.save_path, 'w', encoding='utf-8') as f:
            data = json.dumps(database, indent=4)
            f.write(data)

    def get_page_info(self, page_index):
        if page_index == 1:
            page_url = '{}/{}/{}'.format(self.homepage, self.category_major, self.category_minor)
        else:
            page_url = '{}/{}/{}/index_{}.html'.format(self.homepage, self.category_major, self.category_minor, page_index)

        data = []
        try:
            response = requests.get(page_url, headers=HEADERS)
            response.encoding = self.res_encoding
            soup = BeautifulSoup(response.text, features='lxml')
            items = soup.find_all('dl')
            for item in items:
                item = item.dd.a
                try:
                    title = item.text
                    url = item['href']
                    if not url.endswith('.html'):
                        continue
                    url = self.homepage + url
                    data.append({
                        'url': url, 
                        'title': title
                    })
                except Exception as e:
                    pass
        except Exception as e:
            print('error: ' + str(e))
        
        return data
    
    def get_link(self, video_url):
        links = []
        try:
            response = requests.get(video_url, headers=HEADERS)
            response.encoding = self.res_encoding
            soup = BeautifulSoup(response.text, features='lxml')
            items = soup.find_all(attrs={'class': 'download'})
            # print(items)
            for item in items:
                download_link = item.a['href']
                links.append(download_link)
        except Exception as e:
            print(str(e))

        return links
    
    def run(self, start=1, end=-1):
        current_page = start
        database = self.load_links()
        nvideos = len(database)
        print('{} videos loaded'.format(nvideos))

        while True:
            try:
                print('[page] {}'.format(current_page))
                video_info = self.get_page_info(current_page)
                # print(video_info)
                for info in video_info:
                    title = info['title']
                    print('[video] {}'.format(title))
                    if title in database.keys():
                        continue
                    url = info['url']
                    links = self.get_link(url)
                    if len(links) > 0:
                        database[title] = links

                    ntitles = len(database.keys())
                    if ntitles % 100 == 0:
                        self.save_links(database)
                current_page += 1
                if end > 0 and current_page > end:
                    break
            except KeyboardInterrupt as e:
                print(str(e))
                self.save_links(database)
                break
            except Exception as e:
                print(str(e))


class Hu4VideoDownloader(object):
    def __init__(self):
        pass

    def load_urls(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            database = json.loads(f.read())
        return database

    def download_video(self, video_url, video_path):
        file_path = wget.download(video_url, out=video_path)
        return file_path
    
    def title_simplify(self, title):
        title = title.replace('?', '').replace(':', '').replace('|', '')
        title = title.replace('“', '').replace('”', '').replace(' ', '')
        title = title.replace('/', '')
        return title

    def run(self, json_path, save_root):
        dataset = self.load_urls(json_path)
        for idx, (title, urls) in enumerate(dataset.items()):
            if len(urls) == 0:
                continue
            video_url = urls[0]
            if 'thunder' in video_url:
                continue
            
            # print('downloading {}'.format(title))
            if not os.path.exists(save_root):
                os.makedirs(save_root)
            
            ext = video_url.split('.')[-1]
            title = self.title_simplify(title)
            target_path = os.path.join(save_root, '{}.{}'.format(title, ext))
            if os.path.exists(target_path):
                continue

            # try:
            print('\ndownloading {}\n =====>{}'.format(video_url, target_path))
            self.download_video(video_url, target_path)
            # except Exception as e:
            #     print('download failed: ' + str(e))
