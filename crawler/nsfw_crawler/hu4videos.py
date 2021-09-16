"""
get video download links
"""
import requests
from bs4 import BeautifulSoup
import os
from urllib import request
import time
import json


headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/2.0.0.11'}


class Hu4Video(object):
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
            response = requests.get(page_url, headers=headers)
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
            response = requests.get(video_url, headers=headers)
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


if __name__ == '__main__':
    vid = Hu4Video('movie', 'meiyan', save_path='4hulinks_meiyan.json')
    vid.run()
