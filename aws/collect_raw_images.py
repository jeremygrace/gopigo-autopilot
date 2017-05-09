import os
import cv2
import urllib.request
import numpy as np


def retrieve_raw_images():
    imgs_link = 'http://image-net.org/api/text/' \
                'imagenet.synset.geturls?wnid=n09282208'
    image_url = urllib.request.urlopen(imgs_link).read().decode()
    pic_num = 1

    if not os.path.exists('negative'):
        os.makedirs('negative')

    for img in image_url.split('\n'):
        try:
            print(img)
            urllib.request.urlretrieve(img, "negative/"+str(pic_num)+".jpg")
            image = cv2.imread("negative/"+str(pic_num)+".jpg",
                               cv2.IMREAD_GRAYSCALE)
            resized_image = cv2.resize(image, (100, 100))
            cv2.imwrite("negative/"+str(pic_num)+".jpg", resized_image)
            pic_num += 1

        except Exception as e:
            print(str(e))


def create_neg_txtfile():
    for file_type in ['negative']:
        for img in os.listdir(file_type):
            if file_type == 'negative':
                line = file_type+'/'+img+'\n'
                with open('bg.txt', 'a') as f:
                    f.write(line)


if __name__ == "__main__":
    retrieve_raw_images()
    create_neg_txtfile()
