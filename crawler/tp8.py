
"""
download 
www.tp8.com/yule/meinv
www.tp8.com/yule/rentiyishu
"""
import os
import requests
from bs4 import BeautifulSoup
from urllib import request


headers = {
    'accept': "application/json, text/javascript, */*; q=0.01",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
}


class TPBar(object):
    """
    TODO: HTTP 404: Not Found Error
    """
    def __init__(self, data_root='./tp8', task='meinv'):
        assert task in ['meinv', 'rentiyishu']
        if task == 'meinv':
            task_pages = 639
        else:
            task_pages = 0

        self.data_root = os.path.join(data_root, task)
        self.homepage = 'https://www.tp8.com'
        self.taskpage = '{}/yule/{}'.format(self.homepage, task)

    def crawl_set(self, set_idx, save_folder):
        set_main_url = '{}/{}.html'.format(self.taskpage, set_idx)
        response = requests.get(set_main_url, headers=headers)
        soup = BeautifulSoup(response.text, features='lxml')
        # get num-pages, each page contains 1 image
        page_soup = soup.find(attrs={'class': 'page'})
        npages = 0
        for item in page_soup.find_all('a'):
            if item.text == '末页':
                print(item)
                npages = int(item['href'].split('_')[-1].split('.')[0])
            
        print('npages = ', npages)
        for i in range(1, npages+1):
            self.crawl_image(set_idx, i, save_folder)
    
    def crawl_image(self, set_idx, img_idx, save_folder):
        if img_idx == 1:
            set_img_url = '{}/{}.html'.format(self.taskpage, set_idx)
        else:
            set_img_url = '{}/{}_{}.html'.format(self.taskpage, set_idx, img_idx)
        response = requests.get(set_img_url, headers=headers)
        soup = BeautifulSoup(response.text, features='lxml')
        main = soup.find(attrs={'class': 'pic-main'})
        img_url = main.a.img['src']
        filename = os.path.basename(img_url)
        if filename == '':
            return
        save_path = os.path.join(save_folder, filename)
        print('[IMAGE]{}'.format(img_url))
        # print('save_path: ', save_path)
        self.download_image(img_url, save_path)
    
    def download_image(self, url, save_path):
        try:
            # request.urlretrieve(url, save_path)
            with open(save_path, 'wb') as f:
                req = request.Request(url, headers=headers)
                data = request.urlopen(req).read()
                f.write(data)
        except Exception as e:
            print('download error: ' + str(e))
    
    def run(self, page_idx):
        if page_idx == 1:
            url = self.taskpage
        else:
            url = '{}/page/{}'.format(self.taskpage, page_idx)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, features='lxml')
        w1200_soup = soup.find(attrs={'class': 'l-pub'})
        for item in w1200_soup.find_all('li'):
            href = item.a['href']
            title = item.a['title']
            time_str = item.a.span.text
            set_idx = href.split('/')[-1].split('.')[0]
            save_folder = os.path.join(self.data_root, time_str, title)
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            print('[SET]{}'.format(title))
            self.crawl_set(set_idx, save_folder)
            break


if __name__ == '__main__':
    crawler = TPBar('../data/tp8')
    crawler.run(1)
