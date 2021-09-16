import os
import glob
import tensorflow as tf
from PIL import Image
from tensorflow.contrib.slim.nets import resnet_v1

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
path = "J:\\public\\nsfw_classified_result\\result0812\\collection_all\\"
# classes = ['animationnormal', 'animationporn', 'animationsexy', 'closeaction', 'generalnormal', 'generalporn',
#                'generalsexy', 'lesbianporn', 'malenormal', 'maleporn', 'malesexy', 'sexytoy', 'statueart']


classes = ['malenormal']
def is_valid_jpg(jpg_file):
    with open(jpg_file, 'rb') as f:
        f.seek(-2, 2)
        buf = f.read()
        f.close()
        return buf ==  b'\xff\xd9'  # 判定jpg是否包含结束字段


fn = 'yourimage.JPEG'
init_op = tf.initialize_all_tables()
sess = tf.Session()
sess.run(init_op)


for cls in classes:
    sub = 0
    images = os.listdir(path + cls)
    for img in images:
        #print("folder:{}, image:{}".format(cls, img))
        image_contents = tf.read_file(os.path.join(path, cls, img))
        try:
            image = tf.image.decode_jpeg(image_contents, channels=3)
            tmp = sess.run(image)
        except:
            print("folder:{}, image:{}".format(cls, img))



flag=0
for cls in classes:
    sub = 0
    images = os.listdir(path+cls)
    png = glob.glob(path + cls + "\\*.png")
    for img in images:
        isCompleted = is_valid_jpg(os.path.join(path, cls, img))
        if isCompleted:
            flag +=1
            sub += 1
    print("sub folder {} has {},  completed:{}, has png file:{} ".format(cls, images.__len__(),  sub, png.__len__()))
        #print("image {} is completed:{}".format(img, isCompleted))


print("total {} images, completed {}".format(images.__len__(), flag))
'''
原文：https://blog.csdn.net/kingroc/article/details/86692156 
'''
