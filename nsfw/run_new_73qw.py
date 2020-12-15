import requests
from bs4 import BeautifulSoup
import os
from urllib import request
import time

ROOT_URL = 'http://www.73qw.com'
ROOT_IMAGE_PATH = './image_data_new_73qw'
IMAGE_SITES = ['img6.26ts.com']

ENCODING = 'ISO-8859-1'
RES_ENCODING = 'utf8'

headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; Win64; x64; rv:60.0) \
			Gecko/20100101 Firefox/2.0.0.11'}


def get_time_stamp():
	return time.strftime('%Y%m%d-%H:%M:%S', time.localtime(time.time()))


def check_valid_image_url(url):
	if 'img6' in url:
		return True
	else:
		return False


def get_image_pages(url):
	page_urls = []
	try:
		res = requests.get(url)
	except:
		print('Error')
		return []
	# print(res)

	res.encoding = RES_ENCODING
	soup = BeautifulSoup(res.text, 'html.parser')
	items = soup.select('li')

	for item in items:
		# print(item)
		subs = item.find_all('a')
		if len(subs) == 0:
			continue
		for s in subs:
			href = s.get('href')
			href_parts = href.split('/')
			try:
				idx = int(href_parts[-2])
			except:
				# filter all non-page-links
				continue
			# if href.startswith('/art'):
			text = s.text
			page_urls.append((ROOT_URL + href, text))
	return page_urls


def get_urls_from_page(url):
	image_urls = []
	try:
		res = requests.get(url)
	except:
		print('network error')
		return []

	soup = BeautifulSoup(res.text, 'html.parser')
	items = soup.find_all('img')
	# print(url)
	# print(len(items))
	for item in items:
		img_url = item.get('src')
		# print(img_url)
		if img_url.endswith('.gif'):
			continue
		if check_valid_image_url(img_url):
			image_urls.append(img_url)
	return image_urls


def download_urls(name, image_urls):
	save_path = os.path.join(ROOT_IMAGE_PATH, name)
	if not os.path.exists(save_path):
		os.makedirs(save_path)

	for url in image_urls:
		image_name = os.path.split(url)[-1]
		save_name = os.path.join(save_path, image_name)
		if os.path.exists(save_name):
			continue
		try:
			time_str = get_time_stamp()
			print('{}|downloading: [{}]{}'.format(time_str, name, url))
			
			resp = request.Request(url, headers=headers)
			resp = request.urlopen(resp)
			data = resp.read()
			with open(save_name, 'wb') as f:
				f.write(data)
		except Exception as e:
			print(e)
			continue


def app():
	url_first = 'http://www.73qw.com/art/yazhoutupian/'
	url_tmp = 'http://www.73qw.com/art/yazhoutupian/index_{}.html'
	urls = [url_first]
	start = 2
	end = 1291
	urls.extend([url_tmp.format(i) for i in range(start, end + 1)])
	
	for i, page_url in enumerate(urls):
		# if i == 0:
		# 	# skip first page
		# 	continue

		print('downloading page {}'.format(i))
		url_names = get_image_pages(page_url)
		
		for url, name in url_names:
			print(url, name)
			img_urls = get_urls_from_page(url)
			download_urls(name, img_urls)
			# break
		# break


if __name__ == '__main__':
	app()
