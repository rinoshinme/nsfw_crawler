"""
Run image crawler
"""

# Python3 env
# from nsfw.hentai_cosplay import HentaiCrawler
# from nsfw.qw73 import QW73

# Python2 env
# from normal.baidu import Baidu
import os
from crawler.nsfw import Hu4Image, Hu4Video, Hu4VideoDownloader


ROOT_DIR = r'F:\Data\crawler_data'


def test_hu4():
    category = 'meitui'
    crawler = Hu4Image(category)
    crawler.run(os.path.join(ROOT_DIR, 'hu4', category))


def test_hu4video():
    category_major = 'movie'
    category_minor = 'meiyan'
    json_path = os.path.join(ROOT_DIR, 'hu4video', '{}_{}.json'.format(category_major, category_minor))
    # vid_crawler = Hu4Video(category_major, category_minor, json_path)
    # vid_crawler.run()

    downloader = Hu4VideoDownloader()
    video_folder = os.path.join(ROOT_DIR, 'hu4video', 'movie_meiyan')
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    downloader.run(json_path, video_folder)


def run():
    # crawler = HentaiCrawler('./data/hentai_crawler')
    # crawler.crawl_tag('naked')
    # crawler = Baidu('./data/baidu')
    # crawler = QW73('../../data/QW73', category='meituisiwa')
    # crawler.run()

    # test_hu4()
    test_hu4video()


if __name__ == '__main__':
    run()

