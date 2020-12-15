"""
Baidu Image Crawler
"""
import itertools
import urllib
import requests
import os
import re
from normal.baidu_utils import str_table, char_table

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36 Edg/80.0.361.54' 
}


class Baidu(object):
    def __init__(self, data_root, max_num=1000):
        self.data_root = data_root
        self.char_table = {ord(k): ord(v) for k, v in char_table.items()}
        self.max_page = 100
        self.re_url = re.compile(r'"objURL":"(.*?)"')
        self.max_num = max_num

    def crawl_key(self, keyword):
        save_folder = os.path.join(self.data_root, keyword)
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        urls = self.build_urls(keyword)
        count = 0
        for url in urls:
            print('requesting: ', url)
            html = requests.get(url, timeout=10, headers=headers).content.decode('utf-8')
            img_urls = self.resolve_img_url(html)
            if len(img_urls) == 0:
                continue
            for img_url in img_urls:
                name = str(count) + '.jpg'
                save_path = os.path.join(save_folder, name)
                if self.download_image(img_url, save_path):
                    count += 1
                    print('{} downloaded'.format(count))
                if count > self.max_num:
                    break
        print('{} download success!'.format(keyword))
        print('system end.')

    def crawl_batch(self, keywords_text):
        keys = self.read_keywords(keywords_text)
        for k in keys:
            self.crawl_key(k)

    def read_keywords(self, text_file):
        keys = []
        with open(text_file, 'r') as f:
            for line in f.readlines():
                keys.append(line.strip())
        return keys

    def download_image(self, img_url, file_path):
        try:
            res = requests.get(img_url, timeout=15, headers=headers)
            if str(res.status_code)[0] == '4':
                print(str(res.status_code), ":", img_url)
                return False
        except Exception as e:
            print('failed', img_url)
            print(str(e))
            return False
        
        print(img_url)
        with open(file_path, 'wb') as f:
            f.write(res.content)
        return True

    def resolve_img_url(self, html):
        print(html)
        img_urls = [self.decode(x) for x in self.re_url.findall(html)]
        return img_urls

    def decode(self, url):
        for key, value in str_table.items():
            url = url.replace(key, value)
        return url.translate(self.char_table)
    
    def build_urls(self, word):
        word = urllib.quote(word.decode('gbk').encode('utf-8'))
        url = r'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60'
        urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=self.max_page))
        return urls
