"""
Run image crawler
"""

# Python3 env
# from nsfw.hentai_cosplay import HentaiCrawler
# from nsfw.qw73 import QW73

# Python2 env
# from normal.baidu import Baidu
import os
import random
import multiprocessing
from crawler.nsfw import Hu4Image, Hu4Video, Hu4VideoDownloader
from crawler.nsfw import DigitsSite
from crawler.nsfw import QW73


ROOT_DIR = r'F:\Data\crawler_data'


# -------------------------------------------------------------------
# basic downloaders
def download_hu4(category):
    # category = 'meitui'
    crawler = Hu4Image(category)
    crawler.run(os.path.join(ROOT_DIR, 'hu4', category), start=1)


def download_digits(category):
    # category = 'beauty'
    crawler = DigitsSite(category)
    crawler.run(os.path.join(ROOT_DIR, 'digits', category))


def download_qw73(category):
    crawler = QW73(category)
    crawler.run(os.path.join(ROOT_DIR, 'mv369'))


def download_hu4video(category_major, category_minor):
    # category_major = 'movie'
    # category_minor = 'meiyan'
    json_path = os.path.join(ROOT_DIR, 'hu4video', '{}_{}.json'.format(category_major, category_minor))
    vid_crawler = Hu4Video(category_major, category_minor, json_path)
    vid_crawler.run()


def download_hu4video_real(json_path, video_folder):
    """
    download video files.
    """
    downloader = Hu4VideoDownloader()
    video_folder = os.path.join(ROOT_DIR, 'hu4video', 'movie_meiyan')
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    downloader.run(json_path, video_folder)


# -----------------------------------------------------------------------
# multiprocessing
def test_hu4_mp():
    nprocesses = 12
    categories = ['meitui', 'toupai', 'oumei', 'katong']
    for i in range(nprocesses):
        category = categories[i % len(categories)]
        t = multiprocessing.Process(target=download_hu4, args=(category,))
        t.start()


def test_digits_mp():
    nprocesses = 20
    categories = ['beauty', 'asian', 'hentai', 'basic', 'body', 
                  'highheel', 'network']
    for i in range(nprocesses):
        category = categories[i % len(categories)]
        t = multiprocessing.Process(target=download_digits, args=(category, ))
        t.start()


def test_qw73_mp():
    nprocesses = 20
    categories = ['yazhoutupian', 'oumeitupian', 'meituisiwa', 'toupaizipai', 
                  'qingchunweimei', 'lingleitupian', 'katongtietu', 'shunvluanlun']
    for i in range(nprocesses):
        category = categories[i % len(categories)]
        t = multiprocessing.Process(target=download_qw73, args=(category, ))
        t.start()


def test_hu4video_mp():
    def get_all_pairs(categories):
        pairs = []
        for cat in categories.keys():
            for k in categories[cat]:
                pairs.append((cat, k))
        return pairs
    
    pairs = get_all_pairs(Hu4Video.HU4_VIDEO_CATEGORIES)
    nprocesses = len(pairs)
    for i in range(nprocesses):
        major = pairs[i][0]
        minor = pairs[i][1]
        t = multiprocessing.Process(target=download_hu4video, args=(major, minor))
        t.start()


def run():
    # crawler = HentaiCrawler('./data/hentai_crawler')
    # crawler.crawl_tag('naked')
    # crawler = Baidu('./data/baidu')
    # download_qw73('yazhoutupian')

    # test_hu4_mp()
    test_hu4video_mp()
    # test_digits_mp()
    # test_qw73_mp()


if __name__ == '__main__':
    run()
