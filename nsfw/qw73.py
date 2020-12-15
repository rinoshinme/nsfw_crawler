import requests
from bs4 import BeautifulSoup
import os
from urllib import request
import time

headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/2.0.0.11'}


class QW73(object):
	def __init__(self, save_root, category='yazhoutupian'):
		self.homepage = 'http://www.73qw.com'
		self.category = category
		self.image_site_url = 'img6.26ts.com'
		self.res_encoding = 'utf8'
		self.save_root = save_root
		self.save_folder = os.path.join(self.save_root, self.category)
	
	def get_page_url(self, idx):
		if idx == 1:
			url = '{}/art/{}'.format(self.homepage, self.category)
		else:
			url = '{}/art/{}/index_{}.html'.format(self.homepage, self.category, idx)
		return url

	def run(self, save_folder, start=1, end=1291):
		main_urls = [self.get_page_url(i) for i in range(start, end)]
		for i, page_url in enumerate(main_urls):
			print('[PAGE]{}'.format(page_url))
			set_info = self.get_set_info(page_url)
			break
	
	def cleanup(self, save_folder, start=1, end=1291):
		main_urls = [self.get_page_url(i) for i in range(start, end)]
		import shutil
		for i, page_url in enumerate(main_urls):
			set_info = self.get_set_info(page_url)
			for _, title, date in set_info:
				sub_folder = os.path.join(save_folder, title)
				if os.path.exists(sub_folder):
					# move into date folder
					new_p = os.path.join(save_folder, date)
					if not os.path.exists(new_p):
						os.makedirs(new_p)
					shutil.move(sub_folder, new_p)

	def get_set_info(self, url):
		set_info = []
		try:
			response = requests.get(url, headers=headers)
			response.encoding = self.res_encoding
			soup = BeautifulSoup(response.text, features='lxml')
			container = soup.find(attrs={'id': 'tpl-img-content'})
			for item in container.find_all('li'):
				href = item.a['href']
				title = item.a['title']
				date = item.a.span.text
				print(href)
				print(title)
				print(date)
				set_info.append((href, title, date))
		except Exception as e:
			print('error: ' + str(e))
		return set_info
	
	def crawl_set(self, set_url):
		pass

	def download_image(self, image_url, save_path):
		pass


if __name__ == '__main__':
	crawler = QW73('./data')
	crawler.run('./data')
