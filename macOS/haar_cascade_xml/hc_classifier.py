'''
Author: Jeremy Grace
Reference:
http://docs.opencv.org/3.1.0/dc/d2e/
tutorial_py_image_display.html

 -- Utilized --
Zheng Wang's Haar Cascade Classifier
https://github.com/hamuchiwa/AutoRCCar
'''

import cv2
import numpy as np


# Zheng Wang's Haar Cascade Classifier
# stop_signs = cv2.CascadeClassifier('stop_signs_ZW.xml')

# My trained Haar Cascade Classifier
stop_signs = cv2.CascadeClassifier('stop_signs_JG.xml')

# Grab and initialize macOS camera
cap = cv2.VideoCapture(0)

while True:
    #
    ret, img = cap.read()
    #
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
    signs = stop_signs.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in signs:
        #
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        #
        roi_gray = gray[y:y+h, x:x+w]
        #
        roi_color = img[y:y+h, x:x+w]
    # Display img in window utilize python underhood
    cv2.imshow('img', img)
    wKey = cv2.waitKey(30)
    if wKey == 27:
        break

cap.release()
cv2.destroyAllWindows()
