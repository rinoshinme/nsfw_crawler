import os
import time


def read_image_list(folder, file):
    image_names = []
    file_path = os.path.join(folder, file)
    with open(file_path, 'r', encoding='utf-8') as ff:
        lines = ff.readlines()
        for line in lines:
            image_names.append(line.split('|')[-1].strip())
    print("file {} has {} images".format(file, image_names.__len__()))
    #print(image_names[0:10])
    return image_names


def read_local_images(local_folder):
    local_images = []
    sub_folders = os.listdir(local_folder)
    for folder in sub_folders:
        sub_class = os.path.join(local_folder, folder)
        if os.path.isdir(sub_class):
            local_images.extend(os.listdir(sub_class))
    print("local folder:{} has {} images".format(local_folder, local_images.__len__()))

file_folder = r'J:\datastat'
file_0625 = 'data_0625_image_list.txt'
file_check = 'data_checked_image_list.txt'
file_2627 = 'data_0626_0627_image_list.txt'
file_data = 'data_image_list.txt'
images_0625 = read_image_list(file_folder, file_0625)
images_check = read_image_list(file_folder, file_check)
images_2627 = read_image_list(file_folder, file_2627)
images_data = read_image_list(file_folder, file_data)
set_0625 = set(images_0625)
set_check = set(images_check)
set_2627 = set(images_2627)
set_data = set(images_data)
print("set_0625 len:", set_0625.__len__())
print("set_check len:", set_check.__len__())
print("set_2627 len:", set_2627.__len__())
print("set_data len:", set_data.__len__())

gap0625 = set_0625.difference(set_check)
gap2627 = set_2627.difference(set_check)
gap_data = set_data.difference(set_check)
print("gap 0625 len:", gap0625.__len__())
print("gap 2627 len:", gap2627.__len__())
print("gap data len:", gap_data.__len__())
