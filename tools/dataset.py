import os
from common import is_image_file


def generate_trainval(image_folder, categories, text_path):
    for c in categories:
        sub_folder = os.path.join(image_folder, c)
        for f in os.listdir(sub_folder):
            if not is_image_file(f):
                continue
            fpath = os.path.join(sub_folder, f)



if __name__ == '__main__':
    pass