#-*- encoding: utf-8 -*- 

import requests
import json
from urllib.parse import quote
import urllib.request
import os
 
# 百度图片加密规则
base_encode = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/',
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
    'a': '0',
    '-': '-'
}
objURL = []         # 用于存储json格式的objURL地址
url_list = []       # 用于存储解码后的图片URL地址
 
# 伪装身份与解决防盗链
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
          'Referer': 'https://image.baidu.com/'}
 
# 通过url地址返回网页源码
def get_html(url):
    rep = requests.get(url, headers=header)
    if rep.status_code == 200:
        return rep.text
    else:
        return None
 
# 获取json数据中objURL数据并存至列表中
def get_objURL(html):
    if '\\' in html:
        html = html.replace('\\', '')
 
    # print(html)
    html_lines = html.split('\n')
    for idx, line in enumerate(html_lines):
        if idx != 26:
            continue
        print(idx)
        print(line)
        print(line[150:160])
    
    datas = json.loads(html)
    ress = datas['data'][:-1]
    for res in ress:
        objURL.append(res["objURL"])
 
# 解码objURL地址，并存至解析后的列表中
def parse_strins(objurl):
    if '_z2C$q' in objurl:
        objurl = objurl.replace('_z2C$q', ':')
    if '_z&e3B' in objurl:
        objurl = objurl.replace('_z&e3B', '.')
    if 'AzdH3F' in objurl:
        objurl = objurl.replace('AzdH3F', '/')
 
    res = ''
    for s in objurl:
        if s in base_encode:
            res += base_encode[s]
        else:
            res += s
    url_list.append(res)
 
# 创建并返回图片的存储路径
def create_path(names):
    path = os.path.join(os.getcwd(), '{}'.format(names))
    if not os.path.exists(path):
        os.mkdir(path)
    return path
 
# 实现图片文件的下载
def download_image(path, image_url, i):
    end_type = os.path.splitext(image_url)[-1]
    imageName = os.path.join(path, end_type)
    try:
        urllib.request.urlretrieve(image_url, imageName)
        print('已下载第{}张图片...'.format(i + 1))
    except:
        pass
 
# 实现以上函数的调用与功能的实现

def main2(names, pages):
    path = create_path(names)
    for i in range(pages):
        print('正在爬取第 {} 页的数据...'.format(i + 1))
        page = i * 30
        urls = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={0}=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word={0}&s=&se=&tab=&width=1920&height=1080&face=0&istype=2&qc=&nc=&fr=&expermode=&force=&cg=star&pn={1}&rn=30&gsm=1f'.format(quote(names), page)
 
        print(urls)
        html = get_html(urls)
        if html:
            get_objURL(html)
 
    for obj in objURL:
        parse_strins(obj)
 
    for m in range(len(url_list)):
        download_image(path, url_list[m], m)

def main():
    while True:
        names = input('请输入要查询的关键字：')
        if not names:
            break
        path = create_path(names)
        try:
            pages = int(input('请输入爬取的页码数：'))
        except:
            print('请输入正确的页码数【int】')
            print('-' * 100)
        else:
            for i in range(pages):
                print('正在爬取第 {} 页的数据...'.format(i + 1))
                page = i * 30
                urls = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={0}=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word={0}&s=&se=&tab=&width=1920&height=1080&face=0&istype=2&qc=&nc=&fr=&expermode=&force=&cg=star&pn={1}&rn=30&gsm=1f'.format(quote(names), page)
 
                print(urls)
                html = get_html(urls)
                if html:
                    get_objURL(html)
 
            for obj in objURL:
                parse_strins(obj)
 
            for m in range(len(url_list)):
                download_image(path, url_list[m], m)
 
if __name__ == '__main__':
    # main()
    main2('广告牌', 10)
