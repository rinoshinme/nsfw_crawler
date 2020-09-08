import requests
from bs4 import BeautifulSoup
import re
import os
from urllib import request
import time


# --------------------------------------------------------------------------------------------------------------------
def get_url(cate, start):
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        'cache-control': "no-cache",
        'postman-token': "fab4fce6-bc85-d134-e42e-a73628962c1f"
    }

    imgs = requests.get(
        'https://pic.sogou.com/pics?query=' + cate + '&mode=0&start=' + str(start) + '&reqType=ajax&reqFrom=result&tn=0',
        headers=headers)
    html = BeautifulSoup(imgs.text)

    urls = re.findall("thumbUrl(.*?),", str(html), re.S)
    pic_urls = []
    for url in urls:
        print(url[3:-1])
        pic_urls.append(url[3:-1])
    return pic_urls


def download_pic(pic_urls, cate, page):
    file_path = './data/' + cate + '/'
    print(file_path)
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    m = 48 * page
    for img_url in pic_urls:
        print('***** ' + str(m) + '.jpg *****' + '   Downloading...')
        try:
            request.urlretrieve(img_url, file_path + str(m) + '.jpg')
        except Exception as e:
            print(str(m) + ".jpg下载失败")
        m = m + 1
    print('Download complete!')


if __name__ == "__main__":
    cate = 'dog'
    for i in range(1, 100):
        urls = get_url(cate, i * 48)
        download_pic(urls, cate, i)
