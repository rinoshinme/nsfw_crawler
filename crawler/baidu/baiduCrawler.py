#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: loveNight

import json
import itertools
import urllib
import requests
import os
import re
import sys


str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36 Edg/80.0.361.54' 
}

# str ��translate������Ҫ�õ����ַ���ʮ����unicode������Ϊkey
# value �е����ֻᱻ����ʮ����unicode����ת�����ַ�
# Ҳ����ֱ�����ַ�����Ϊvalue
char_table = {ord(key): ord(value) for key, value in char_table.items()}

# ����ͼƬURL
def decode(url):
    # ���滻�ַ���
    for key, value in str_table.items():
        url = url.replace(key, value)
    # ���滻ʣ�µ��ַ�
    return url.translate(char_table)

# ������ַ�б�
def buildUrls(word):
    word = urllib.quote(word.decode('gbk').encode('utf-8'))
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls

# ����JSON��ȡͼƬURL
re_url = re.compile(r'"objURL":"(.*?)"')
#re_url = re.compile(r'"objURL":".*/(.*?)"')
#re_url = re.compile(r'.*/(.*?)\.jpg',re.S)
def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls

def downImg(imgUrl, dirpath, imgName):
    filename = os.path.join(dirpath, imgName)
    try:
        res = requests.get(imgUrl, timeout=15, headers=headers)
        if str(res.status_code)[0] == "4":
            print(str(res.status_code), ":" , imgUrl)
            return False
    except Exception as e:
        print("failed", imgUrl)
        print(e)
        return False
    print(imgUrl)
    with open(filename, "wb") as f:
        f.write(res.content)
    return True


def mkDir(dirName):
    dirpath = os.path.join(sys.path[0], dirName)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath


def download_keyword(keyword, savepath, downloadnum):
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    urls = buildUrls(keyword)
    index = 0
    
    for url in urls:
        print("Requesting: ", url)
        html = requests.get(url, timeout=10, headers=headers).content.decode('utf-8')
        imgUrls = resolveImgUrl(html)
        if len(imgUrls) == 0:
            break
        for url in imgUrls:
            name = str(index) + '.jpg'
            if downImg(url, savepath, name):
                index += 1
                print("%s downloaded." % index)

            if index > downloadnum:
                return
    print(keyword,' suceess download!')
    print('system end')


def read_keywords(key_txt):
    keys = []
    with open(key_txt, 'r') as f:
        for line in f.readlines():
            keys.append(line.strip())
    return keys


if __name__ == '__main__':
    key_txt = './keywords.txt'
    keywords = read_keywords(key_txt)

    downloadnum = 500
    for idx, k in enumerate(keywords):
        print(k)
        download_path = './data/' + k + '/'
        download_keyword(k, download_path, downloadnum)
        # if idx == 2:
        #     break
