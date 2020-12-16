"""
Run image crawler
"""

# Python3 env
# from nsfw.hentai_cosplay import HentaiCrawler
from nsfw.qw73 import QW73

# Python2 env
# from normal.baidu import Baidu


def run():
    # crawler = HentaiCrawler('./data/hentai_crawler')
    # crawler.crawl_tag('naked')
    # crawler = Baidu('./data/baidu')
    crawler = QW73(r'F:/data/porn/qw73')
    crawler.run()


if __name__ == '__main__':
    run()

