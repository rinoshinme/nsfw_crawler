import os
import requests
from bs4 import BeautifulSoup
from urllib import request


headers = {
    'accept': "application/json, text/javascript, */*; q=0.01",
    'x-requested-with': "XMLHttpRequest",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    'cache-control': "no-cache",
    'postman-token': "fab4fce6-bc85-d134-e42e-a73628962c1f"
}


class HentaiCrawler(object):
    def __init__(self, data_root='./hentai_cosplay'):
        self.homepage = 'https://hentai-cosplays.com/'
        self.data_root = data_root
        self.tag_pages = 896  # total number of tag pages
    
    def get_tags(self, tag_page):
        tags = []
        tag_url = '{}/tag/page/{}/'.format(self.homepage, tag_page)
        response = requests.get(tag_url, headers=headers)
        soup = BeautifulSoup(response.text, features='lxml')
        tags_item = soup.find(attrs={'id': 'tags'})
        for item in tags_item.find_all('li'):
            tag_url = item.a['href']
            tag = tag_url.split('/')[-2]
            if tag == '':
                continue
            tags.append(tag)
        return tags

    def get_all_tags(self):
        all_tags = []
        for i in range(1, self.tag_pages):
            tgs = self.get_tags(i)
            all_tags.extend(tgs)
        return all_tags
    
    def num_pages_for_tag(self, tag):
        try:
            tag_home = '{}/search/tag/{}'.format(self.homepage, tag)
            response = requests.get(tag_home, headers=headers)
            soup = BeautifulSoup(response.text, features='lxml')
            item = soup.find(attrs={'class':'last'})
            num_pages = int(item['href'].split('/')[-2])
        except Exception as e:
            print('error: ' + str(e))
            return 0
        return num_pages
    
    def crawl_item(self, title):
        item_url = '{}/image/{}'.format(self.homepage, title)
        # find how many pages for this item.
        response = requests.get(item_url, headers=headers)
        soup = BeautifulSoup(response.text, features='lxml')
        for item in soup.find_all('span'):
            if item.text != 'last>>':
                continue
            try:
                u = item.a['href']
                npages = int(u.split('/')[-2])
            except:
                npages = 1
        save_folder = os.path.join(self.data_root, title)
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        print('[TITLE]{}'.format(title))
        
        for i in range(1, npages + 1):
            print('[IMAGE-PAGE]{}/{}'.format(i, npages))
            self.crawl_item_page(title, i, save_folder)

    def crawl_item_page(self, title, page, save_folder):
        """
        each item may split into several pages
        """
        if page == 1:
            url = '{}/image/{}/'.format(self.homepage, title)
        else:
            url = '{}/image/{}/page/{}/'.format(self.homepage, title, page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, features='lxml')
        # get image links
        for item in soup.find_all(attrs={'class': 'icon-overlay'}):
            img_url = item.a.img['src']
            filename = os.path.basename(img_url)
            if filename == '':
                continue
            save_path = os.path.join(save_folder, filename)
            print('[IMAGE]{}'.format(img_url))
            if not os.path.exists(save_path):
                self.download_image(img_url, save_path)

    def crawl_tag(self, tag):
        num_pages = self.num_pages_for_tag(tag)
        for i in range(1, num_pages+1):
            page_url = '{}/search/tag/{}/page/{}/'.format(self.homepage, tag, i)
            # get item urls
            response = requests.get(page_url, headers=headers)
            soup = BeautifulSoup(response.text, features='lxml')
            center_item = soup.find(id='center')
            main_body = center_item.find(attrs={'id':'display_area_image'})
            for item in main_body.find_all(attrs={'class':'image-list-item-image'}):
                item_url = item.a['href']
                title = item_url.split('/')[-2]
                self.crawl_item(title)

    def download_image(self, url, save_path):
        try:
            # request.urlretrieve(url, save_path)
            with open(save_path, 'wb') as f:
                req = request.Request(url, headers=headers)
                data = request.urlopen(req).read()
                f.write(data)
        except Exception as e:
            print('download error: ' + str(e))


if __name__ == '__main__':
    crawler = HentaiCrawler(r'E:\data\porn\hentai_cosplay')
    # crawler.crawl_item('the-omega--the-acc--in-the-first-')
    crawler.crawl_tag('bikini')
    # tags = crawler.get_tags(1)
    # print(tags)
