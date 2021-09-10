"""

"""
import os
import requests


HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
               "Content-Type": 'application/json'}


def download_image(url, save_folder='./images'):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    try:
        image_name = os.path.basename(url)
        save_path = os.path.join(save_folder, image_name)
        res = requests.get(url, timeout=15, headers=HEADERS)
        with open(save_path, 'wb') as f:
            f.write(res.content)
    except Exception as e:
        print('download error: {}'.format(str(e)))


def test():
    # url = 'http://api.btstu.cn/sjbz/?lx=dongman'
    # url = 'http://api.btstu.cn/sjbz/?lx=meizi'
    url = 'http://api.btstu.cn/sjbz/?lx=suiji'
    # url = 'http://api.btstu.cn/sjbz/?lx=m_dongman'
    # url = 'http://api.btstu.cn/sjbz/?lx=m_meizi'
    # url = 'http://api.btstu.cn/sjbz/zsy.php'
    r = requests.get(url, headers=HEADERS)
    image_url = r.url
    download_image(image_url)


if __name__ == '__main__':
    test()
