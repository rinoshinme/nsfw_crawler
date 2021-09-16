import shutil
import os

img_folder = 'J:\\public\\famous_recognition_test_images_0806\\'
subclass = os.listdir(img_folder)
moved_class = 'generalnormal'

target = os.path.join(img_folder, moved_class)
if os.path.exists(target):
    print("target exists")
else:
    os.mkdir(target)

count = 0
for tag in subclass:
    images = os.listdir(os.path.join(img_folder, tag))
    count = count + images.__len__()
    print("under folder:{} has:{} images".format(tag, images.__len__()))
    for image in images:
        f_img = os.path.join(img_folder, tag, image)
        t_img = os.path.join(target, image)
        shutil.move(f_img, t_img)

print("total:", count)
