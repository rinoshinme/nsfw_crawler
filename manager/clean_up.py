import cv2
import os
import hashlib
import shutil


def is_valid_image_file(file_path):
    """
    check if the image file is valid
    """
    if not os.path.isfile(file_path):
        return False
    
    try:
        image = cv2.imread(file_path)
        if image is None:
            return False
        return True
    except Exception as e:
        print('file error: ' + str(e))
    return False


def file_md5(file_path):
    m = hashlib.md5()
    with open(file_path, 'rb') as f:
        data = f.read()
    m.update(data)
    return m.hexdigest()


def rename_to_md5(file_path):
    md5_val = file_md5(file_path)
    file_name = os.path.basename(file_path)
    root, ext = os.path.splitext(file_name)
    if root == md5_val:
        return
    new_path = file_path.replace(root, md5_val)
    if not os.path.exists(new_path):
        shutil.move(file_path, new_path)
    else:
        print('filename exists')


def file_creation_time(file_path):
    pass
