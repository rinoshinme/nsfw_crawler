import os

IMG_EXTS = ['.jpg', '.png', 'bmp', ]


def is_image_file(file_path):
    bname = os.path.basename(file_path)
    ext = bname.split('.')[-1]
    if ext.lower() in IMG_EXTS:
        return True
    else:
        return False
    
