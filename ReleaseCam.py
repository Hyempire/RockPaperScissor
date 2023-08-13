import os
os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'


import cv2
cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
cap.release()
# success, image = cap.read()

print(cap.isOpened())
