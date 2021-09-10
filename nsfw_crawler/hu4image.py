import requests
from bs4 import BeautifulSoup
import os
from urllib import request
import time

headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/2.0.0.11'}


def simplify_title(title):
    title = title.replace('?', '')
    return title


class FourHuImages(object):
    def __init__(self, save_root, category='meitui'):
        """
        categories: ['meitui', 'toupai', 'oumei', 'katong']
        """
        self.homepage = 'https://www.4huxx339.com/'
        self.category = category
        self.save_root = save_root
        self.res_encoding = 'utf-8'

    def run(self, start_page=1, end_page=-1):
        current_page = start_page
        while True:
            print('downloading page {}'.format(current_page))
            set_infos = self.get_page_info(current_page)
            for info in set_infos:
                set_url = info['url']
                title = info['title']
                title = simplify_title(title)
                print('[set] {}'.format(title))
                image_urls = self.get_set_info(set_url)
                for imgurl in image_urls:
                    save_name = os.path.basename(imgurl)
                    save_folder = os.path.join(self.save_root, title)
                    if not os.path.exists(save_folder):
                        os.makedirs(save_folder)
                    save_path = os.path.join(save_folder, save_name)
                    if not os.path.exists(save_path):
                        print('[image]{}'.format(imgurl))
                        self.download_image(imgurl, save_path)
            current_page += 1
            if end_page > 0 and current_page > end_page:
                break


    def get_page_info(self, page_index):
        if page_index == 1:
            page_url = '{}/pic/{}'.format(self.homepage, self.category)
        else:
            page_url = '{}/pic/{}/index_{}.html'.format(self.homepage, self.category, page_index)

        data = []
        try:
            response = requests.get(page_url, headers=headers)
            response.encoding = self.res_encoding
            soup = BeautifulSoup(response.text, features='lxml')
            items = soup.find_all('dl')
            for item in items:
                item = item.dd.a
                try:
                    title = item['title']
                    url = item['href']
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
    
    def get_set_info(self, set_url):
        image_urls = []
        try:
            response = requests.get(set_url, headers=headers)
            response.encoding = self.res_encoding
            soup = BeautifulSoup(response.text, features='lxml')
            container = soup.find(attrs={'class': 'pic'})

            for d in container.find_all('img'):
                image_urls.append(d['src'])

        except Exception as e:
            print('error: ' + str(e))
        
        return image_urls
    
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
    
    crawler = FourHuImages('./4hu', 'meitu')

    crawler.run()
