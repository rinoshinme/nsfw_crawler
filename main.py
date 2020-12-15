"""
Run image crawler
"""

# Python3 env
# from nsfw.hentai_cosplay import HentaiCrawler

# Python2 env
from normal.baidu import Baidu

def run():
    # crawler = HentaiCrawler('./data/hentai_crawler')
    # crawler.crawl_tag('naked')
    crawler = Baidu('./data/baidu')
    crawler.crawl_key('happy')


if __name__ == '__main__':
    run()

