'''
Author: Jeremy Grace
Reference:
http://docs.opencv.org/3.1.0/dc/d2e/
tutorial_py_image_display.html

 -- Utilized --
Zheng Wang's Haar Cascade Classifier
https://github.com/hamuchiwa/AutoRCCar
'''

import time
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 34
rawCapture = PiRGBArray(camera, size=(640, 480))
# Zheng Wang's Haar Cascade Classifier
stop_signs = cv2.CascadeClassifier('stop_signs_ZW.xml')
# My trained Haar Cascade Classifier
# stop_signs = cv2.CascadeClassifier('stop_signs_JG.xml')

# Allow the picamera to warmup
time.sleep(0.1)

while True:
    # Establish capture pipeline of frames from the camera
    for frame in camera.capture_continuous(rawCapture,
                                           format="bgr", use_video_port=True):
        # Capture the raw NumPy array representing the image,
        # Initialize the timestamp,
        # and occupied/unoccupied text
        image = frame.array
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        signs = stop_signs.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in signs:
            #
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            #
            roi_gray = gray[y:y+h, x:x+w]
            #
            roi_color = image[y:y+h, x:x+w]
        # Display Frame in window utilize python underhood
    cv2.imshow("Frame", image)
    wKey = cv2.waitKey(30) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if wKey == ord("q"):
        break
# Perform cleanup after rendering
cv2.destroyAllWindows()
