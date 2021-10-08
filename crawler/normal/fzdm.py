import requests
from bs4 import BeautifulSoup
import os
from urllib import request
import time

ROOT_IMAGE_PATH = './image_data_fzdm'
ENCODING = 'ISO-8859-1'

headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; Win64; x64; rv:60.0) \
			Gecko/20100101 Firefox/2.0.0.11'}

s = requests.session()
s.keep_alive = False


def download_set(root, manga_id, set_id, num_page):
	set_id = str(set_id)
	set_url = '/'.join([root, manga_id, str(set_id)])
	# pages = ['{}/index_{}'.format(set_url, idx) for idx in range(num_page)]
	save_folder = os.path.join(ROOT_IMAGE_PATH, manga_id, set_id)
	if not os.path.exists(save_folder):
		os.makedirs(save_folder)

	for i in range(1, num_page):
		page_url = '{}/index_{}.html'.format(set_url, i)
		save_path_tmpl = os.path.join(save_folder, '%02d_{}.jpg' % i)
		# download page
		try:
			download_page(page_url, save_path_tmpl)
		except Exception as e:
			print(e)
		break


def download_page(page_url, save_path_template):
	print('downloading from {}'.format(page_url))
	try:
		res = requests.get(page_url)
	except Exception as e:
		print(e)
		return
	res.encoding = ENCODING
	# print(res.text)

	parts = res.text.split('"')
	imgs = ['http://www-mipengine-org.mipcdn.com/i/p3.manhuapan.com/' + p for p in parts if 'jpg' in p]
	print(imgs)
	for idx, img in enumerate(imgs):
		print('downloading {}'.format(img))
		download_image(img, save_path_template.format(idx))


def download_image(image_url, save_path):
	try:
		resp = request.Request(image_url, headers=headers)
		resp = request.urlopen(resp)
		data = resp.read()
		with open(save_path, 'wb') as f:
			f.write(data)
	except Exception as e:
		print(e)
		print('{} not downloaded'.format(image_url))
	
	time.sleep(0.1)


if __name__ == '__main__':
	root = 'https://manhua.fzdm.com'
	manga_id = '2'
	num_pages = 25
	for set_id in range(936, 980):
		download_set(root, manga_id, set_id, num_pages)
		break
