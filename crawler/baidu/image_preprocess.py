import os
import cv2
import os
import multiprocessing
import time


log_info = []
dt = '_june26_27'


def validate_dataset(src_dir, dst_dir, class_names):
    start = time.time()
    pid = os.getpid()
    src_path = os.path.join(src_dir, class_names)
    dst_path = os.path.join(dst_dir, class_names)
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    files = os.listdir(src_path)

    num = files.__len__()
    flag = 0
    for f in files:
        print('pid-{} processing for class {} at {}/{}:{}'.format(pid, class_names, flag, num, f))
        # base_name = f.split('.')[0]
        src_file = os.path.join(src_path, f)
        # print(src_file)
        dst_name = class_names+'_'+str(flag)
        ext = f.split('.')[-1]
        img = cv2.imread(src_file)
        # print(img)

        if img is None:
            continue

        dst_file = os.path.join(dst_path, dst_name + '.jpg')
        cv2.imwrite(src_file, img)
        flag = flag + 1

    print("pid-{} Validated {} images on class {}.Time used:{}".format(pid, flag, class_names, time.time() - start))
    log_info.append("pid-{} Validated {} images on class {}.Time used:{}".format(pid, flag, class_names, time.time() - start))


if __name__ == '__main__':
    src_path = 'J:\\public\\nsfw_classified_result\\result0708\\collection_all\\'
    dst_path = 'J:\\public\\nsfw_classified_result\\result0708\\collection_all\\'
    classes = ['animationnormal', 'animationporn', 'animationsexy', 'closeaction', 'generalnormal', 'generalporn',
               'generalsexy', 'lesbianporn', 'malenormal', 'maleporn', 'malesexy', 'sexytoy', 'statueart']

    for clss in classes:
        p = multiprocessing.Process(target=validate_dataset, args=(src_path, dst_path, clss))
        p.start()

    if log_info.__len__() == classes.__len__():
        for log in log_info:
            print(log)

