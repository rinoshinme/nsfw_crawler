"""
https://github.com/rizuzero/nsfw_scraper/blob/master/pixiv_nsfw_image_scraper.py
"""
import json
import os
import getpass
import os
os.system('pip install pixivpy')
from pixivpy3 import *


download_path = './nsfw_download'
print("halo")
def download_rizu_bookmark(api):
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    download_bookmark(api, download_path, 31354730)

def your_bookmark(api, login):
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    user_id = login["user"]["id"]
    download_bookmark(api, download_path, user_id)

def rank(aapi, mode):
    i = True
    try:
        print("Tekan ctrl + c untuk membatalkan download")
        print("Sedang mendownload...")
        
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        json_result = aapi.ranking_all(mode=mode, page=1)
        illust = json_result.response[0].works
        for i in illust:
            aapi.download(i.work.image_urls['large'],path=download_path)
        for x in range(1,json_result.pagination.pages):
            json_result = aapi.ranking_all(mode=mode, page=x)
            illust = json_result.response[0].works
            for i in illust:
                aapi.download(i.work.image_urls['large'], path=download_path)
    except KeyboardInterrupt:
        print("Download dibatalkan")

def download_bookmark(api, download_path, user_id):
    json_result = api.user_bookmarks_illust(user_id)
    i = True
    try:
        while i == True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Tekan ctrl + c untuk membatalkan download")
            print("Sedang mendownload...")
            next_qs = api.parse_qs(json_result.next_url)
            if next_qs != None:
                json_result = api.user_bookmarks_illust(**next_qs)
                for illust in json_result.illusts:
                    api.download(illust.image_urls.large, path=download_path)
            else:
                i = False
    except KeyboardInterrupt:
        print("Download dibatalkan")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("----- Pixiv NSFW scraper created by Rizu ----- \n")
    print("----- ( W A R N I N G!!!) Mengandung gambar NSFW/Hentai ----- \n")
    
    api = AppPixivAPI()
    aapi = PixivAPI()
    auth = True
    show_logged_in = True
    
    while auth == True:
        username = input("Masukkan email pixiv : ")
        password = getpass.getpass("Masukkan password pixiv : ")

        try:
            login = api.login(username, password)
            login_aapi = aapi.login(username, password)
            os.system('cls' if os.name == 'nt' else 'clear')
            ok = True
            while ok == True:
                print("----- Pixiv NSFW scraper created by Rizu ----- \n")
                print("----- ( W A R N I N G!!!) Mengandung gambar NSFW/Hentai ----- \n")
                if show_logged_in == True:
                    print("\n Login berhasil! \n")
                    show_logged_in = False
                
                print("1. Download bookmark Rizu")
                print("2. Download bookmarkmu")
                print("3. Download ranking r18 harian")
                print("4. Download ranking r18 mingguan")
                print("5. Ganti akun")
                print("\n Note: Gambar akan tersimpan di folder nsfw_download")

                case = input("\n Masukkan pilihan : ")
                if case == '1':
                    download_rizu_bookmark(api)

                if case == '2':
                    your_bookmark(api, login)

                if case == '3':
                    mode = "daily_r18"
                    rank(aapi,mode)

                if case == '4':
                    mode = "weekly_r18"
                    rank(aapi,mode)

                if case == '5':
                    ok = False

        except:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n Login gagal! \n")