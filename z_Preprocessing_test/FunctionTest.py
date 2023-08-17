import cv2
import mediapipe as mp
import numpy as np
import ImageProcessing


# ===== Image Processing ===== #
roi = cv2.imread('captured.png')  # for testing with still image
height, width, _ = roi.shape
center_color = roi[height//2, width//2]
print(f"Center color : {center_color}")

resultImage = ImageProcessing.DeleteBackground(roi, center_color, 7, 70, 300)

cv2.imwrite('FunctionTestImage.png', resultImage)