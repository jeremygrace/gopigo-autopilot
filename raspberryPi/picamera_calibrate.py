#!/usr/local/bin/python3.5
"""
References:
-- OpenCV-Python Tutorials: Camera Calibration and 3D Reconstruction
http://opencv-python-tutroals.readthedocs.org/en/latest/
py_tutorials/py_calib3d/py_calibration/py_calibration.html

-- Zheng Wang: hamuchiwa/AutoRCCar/computer/picam_calibration.py
https://github.com/hamuchiwa/AutoRCCar/tree/master/computer
"""

import numpy as np
import cv2
import glob2

# Termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
obj_pt = np.zeros((6 * 9, 3), np.float32)
obj_pt[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
object_points = []  # 3d point in real world space
img_points = []  # 2d points in image plane.
h, w = 0, 0

chessbd_imgs = glob2.glob('chessboard/*.jpg')

for fname in chessbd_imgs:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape[:2]
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

    # If found, add object points, image points (after refining them)
    if ret:
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        img_points.append(corners)
        object_points.append(obj_pt)
        # Draw and display the corners
        cv2.drawChessboardCorners(img, (9, 6), corners, ret)
        cv2.imshow('image', img)
        cv2.waitKey(500)
# calibration
retval, mtx, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(object_points,
                                                            img_points,
                                                            (w, h),
                                                            None, None)

print("Camera Matrix:\n", mtx)

# pi camera intrinsic parameters
ay = mtx[1, 1]
u0 = mtx[0, 2]
v0 = mtx[1, 2]
print("Ay:", ay)
print("u0:", u0)
print("v0:", v0)

cv2.destroyAllWindows()
