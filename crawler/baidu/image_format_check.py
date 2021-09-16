import fleep
import os
import shutil
import time

img_folder ="J:\\public\\nsfw_classified_result\\result0807\\collection_all\\"
# img_folder = 'J:\\public\\famous_recognition_test_images_0806\\'
classes = ['animationnormal', 'animationporn', 'animationsexy', 'closeaction', 'generalnormal', 'generalporn',
               'generalsexy', 'lesbianporn', 'malenormal', 'maleporn', 'malesexy', 'sexytoy', 'statueart',
           'children', 'pornass', 'femalenormal']
subclass = os.listdir(img_folder)
mime = ['image/jpeg', 'image/png']
otherformat = 'otherformat'

start = time.time()
if os.path.exists(img_folder+otherformat):
    pass
else:
    os.mkdir(img_folder+otherformat)

total = 0
flag = 0


for tag in classes:
    images = []
    try:
        images = os.listdir(os.path.join(img_folder, tag))
    except Exception as e:
        print(e)

    total += images.__len__()
    print("checking folder:{} has {}".format(os.path.join(img_folder, tag), images.__len__()))
    for image in images:
        with open(os.path.join(img_folder, tag, image), "rb") as file:
            info = fleep.get(file.read(128))
        if info.mime_matches('image/jpeg') or info.mime_matches('image/png'):
            pass
        else:
            flag += 1
            print("{} format is {}, not jpg or png:".format(os.path.join(tag, image), info.mime))
            f_img = os.path.join(img_folder, tag, image)
            t_img = os.path.join(img_folder, otherformat, image)
            shutil.move(f_img, t_img)

print("total:{} images, other format image count:{}, time used:{} sec".format(total, flag, int(time.time() - start)))

# from: https://swift.ctolib.com/floyernick-fleep.html
# print(info.__str__())
# print(info.type)  # prints ['raster-image']
# print(info.extension)  # prints ['png']
# print(info.mime)  # prints ['image/png']
#
# print(info.type_matches("raster-image"))  # prints True
# print(info.extension_matches("gif"))  # prints False
# print(info.mime_matches("image/png"))  # prints True
# print(info.mime_matches("image/jpeg"))  # prints True