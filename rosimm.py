import os
import time
# import threading
from multiprocessing import Pool, cpu_count
import requests
from bs4 import BeautifulSoup


HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': "http://www.rosimm8.com"
}

ROSIMM_SITE = ''


class RosiCrawler(object):
    def __init__(self):
        self.main_site = 'http://www.rosi263.com'
        self.set_sub = 'rosi_mm'
        self.download_root = './images'
        # self.lock = threading.Lock()
        
        requests.adapters.DEFAULT_RETRIES = 5
        requests.session().keep_alive = False

    def get_set_url(self, set_id):
        return '{}/{}/{}'.format(self.main_site, self.set_sub, set_id)

    def download_image(self, image_url, image_path):
        try:
            print('downloading {}'.format(image_url))
            img = requests.get(image_url, headers=HEADERS, timeout=10)
            with open(image_path, 'ab') as f:
                f.write(img.content)
        except Exception as e:
            print('download error: ' + str(e))
        time.sleep(0.1)
    
    def download_set(self, base_url):
        try:
            r = requests.get(base_url + '.html', headers=HEADERS, timeout=10).text
            soup = BeautifulSoup(r, 'lxml')
            folder_name = soup.find('h1',class_='article-title').find('a').text.encode('ISO-8859-1').decode('utf-8')
            print(folder_name)
            save_folder = os.path.join(self.download_root, folder_name)
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            num_pages = int(soup.find('div',class_='pagination2').find_all('li')[-2].find('a').get_text())
            page_urls = []
            for i in range(1, num_pages + 1):
                if i == 1:
                    page_urls.append(base_url + '.html')
                else:
                    page_urls.append('{}_{}.html'.format(base_url, i))

            # download each page
            image_index = 0
            for page_url in page_urls:
                result = requests.get(page_url, headers=HEADERS, timeout=10).text
                page_soup = BeautifulSoup(result, 'lxml')
                img_urls = page_soup.find('article',class_='article-content').find_all('img')
                for img_url in img_urls:
                    img_url = img_url.get('src')
                    img_url = '{}{}'.format(self.main_site, img_url)
                    img_name = os.path.basename(img_url)
                    save_name = '{:04d}_{}'.format(image_index, img_name)
                    image_index += 1
                    save_path = os.path.join(save_folder, save_name)
                    if os.path.exists(save_path):
                        continue

                    self.download_image(img_url, save_path)

        except Exception as e:
            print('download error: ' + str(e))

    def download_batch(self, start_index=1, end_index=1000):
        for i in range(start_index, end_index):
            url = self.get_set_url(i)
            self.download_set(url)

    def download_batch_mp(self, start_index=1, end_index=1000, nprocesses=0):
        if nprocesses <= 0 or nprocesses > cpu_count():
            nprocesses = cpu_count()
        pool = Pool(processes=nprocesses)
        urls = [self.get_set_url(i) for i in range(start_index, end_index)]
        pool.map(self.download_set, urls)


if __name__ == '__main__':
    crawler = RosiCrawler()
    crawler.download_batch(416, 2528)
    # crawler.download_batch_mp(416, 2528)
