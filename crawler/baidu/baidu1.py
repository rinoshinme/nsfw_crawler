import requests
import re
import os


def get_page_url(url, param):
    response = requests.get(url, params=param)
    response.encoding = 'utf-8'
    return response.text


def parse_page(str):
    pattern = re.compile('"middleURL":"(.*?)",')#利用正则匹配图片url
    url_list = re.findall(pattern, str)
    return url_list


def run(keyword, path):
    url = "https://image.baidu.com/search/acjson"
    i = 0
    for j in range(30, 270, 30):
        params = {"ipn": "rj", "tn": "resultjson_com", "word": keyword, "pn": str(j)}
        html = get_page_url(url, params)
        lists = parse_page(html)
        print(lists)
        for item in lists:
            try:
                img_data = requests.get(item, timeout=10).content
                with open(path + "/" + str(i) + ".jpg", "wb") as f:
                    f.write(img_data)
                    f.close()
                i = i+1
            except requests.exceptions.ConnectionError:
                print('can not download')
                continue


def make_dir(keyword):
    path = "D:/百度图片/"
    path = path+keyword
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
        return path
    else:
        print(path + '目录已存在')
        return path


def main():
    keyword = input("input keyword about images you want to download: ")
    path = make_dir(keyword)
    run(keyword, path)


if __name__ == '__main__':
    main()
