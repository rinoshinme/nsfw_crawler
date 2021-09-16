import json
import wget
import os


class Hu4VideoDownloader(object):
    def __init__(self):
        pass

    def load_urls(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            database = json.loads(f.read())
        return database

    def download_video(self, video_url, video_path):
        file_path = wget.download(video_url, out=video_path)
        return file_path

    def run(self, dataset, save_root):
        for idx, (title, urls) in enumerate(dataset.items()):
            if len(urls) == 0:
                continue
            video_url = urls[0]
            if 'thunder' in video_url:
                continue
            
            print('downloading {}'.format(title))
            if not os.path.exists(save_root):
                os.makedirs(save_root)
            target_path = os.path.join(save_root, title)
            if os.path.exists(target_path):
                continue

            self.download_video(video_url, target_path)

if __name__ == '__main__':
    downloader = Hu4VideoDownloader()
    category = 'wuma'
    database = downloader.load_urls('./4hulinks_{}.json'.format(category))
    # print(database)
    downloader.run(database, '../../crawler_data/hu4_videos/{}'.format(category))
