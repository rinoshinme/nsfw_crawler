from urllib import request


# headers = {
#     'accept': "application/json, text/javascript, */*; q=0.01",
#     'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
# }

headers = {
    'accept': "application/json, text/javascript, */*; q=0.01",
    'x-requested-with': "XMLHttpRequest",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    'cache-control': "no-cache",
    'postman-token': "fab4fce6-bc85-d134-e42e-a73628962c1f"
}


def download_image(image_url, image_path):
    try:
        # request.urlretrieve(url, save_path)
        with open(image_path, 'wb') as f:
            req = request.Request(image_url, headers=headers)
            data = request.urlopen(req).read()
            f.write(data)
        return True
    except Exception as e:
        print('download error: ' + str(e))
    return False
