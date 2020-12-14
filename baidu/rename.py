# -*- encoding: utf-8
import os
import shutil


def rename_files(folder, name):
	files = os.listdir(folder)
	for f in files:
		target = '{}_{}'.format(name, f)
		src_path = os.path.join(folder, f)
		dst_path = os.path.join(folder, target)
		shutil.move(src_path, dst_path)


if __name__ == '__main__':
	folders = ['xingshizheng', 'jiashizheng', 'jiehunzheng', 'shouju']
	names = ['XSZ', 'JSZ', 'JHZ', 'SJ']
	for (folder, name) in zip(folders, names):
		rename_files(folder, name)
