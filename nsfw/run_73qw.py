import requests
from bs4 import BeautifulSoup
import os
from urllib import request
import time

ROOT_URL = 'http://www.73qw.com'
ROOT_IMAGE_PATH = './image_data_73qw'
IMAGE_SITES = ['img6.26ts.com']

ENCODING = 'ISO-8859-1'

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
	res.encoding = 'gb2312'
	soup = BeautifulSoup(res.text, 'html.parser')
	items = soup.select('.listt')

	for item in items:
		subs = item.find_all('a')
		for s in subs:
			href = s.get('href')
			if href.startswith('/html'):
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
	for item in items:
		img_url = item.get('src')
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


def app_old():
	url_head = 'http://www.73qw.com/html/part/16'
	main_url_pages = [url_head + '.html']
	main_url_pages.extend([url_head + "_" + str(i) + '.html' for i in range(2, 3418)])

	for i, page_url in enumerate(main_url_pages):
		print('downloading page {}'.format(i))
		url_names = get_image_pages(page_url)
		print(url_names)
		
		for url, name in url_names:
			img_urls = get_urls_from_page(url)
			print(img_urls)
			download_urls(name, img_urls)


if __name__ == '__main__':
	app_old()
