"""
파일 하나만 넣어서 배경 제거 잘 되는지 테스트하는 코드
"""

import cv2
import mediapipe as mp
import numpy as np
import os
import ImageProcessing

# Mediapipe, Camera Settings
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
# Open Hand module
hands = mp_hands.Hands(max_num_hands = 1,
                 min_detection_confidence = 0.5,
                 min_tracking_confidence = 0.5)

# ========== 테스트 해보고싶은 파일의 경로를 여기다가 넣어주세용 ========== #
image = cv2.imread("./hyemi/rock_captures/hyemi_rock_1.png")
height, width, _ = image.shape

# Hand Tracking
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = hands.process(image)
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

# Find hand color
for hand_landmarks in results.multi_hand_landmarks:
    if results.multi_hand_landmarks:
        colors = []
        for i in range(len(hand_landmarks.landmark)):
            colors.append(image[int(hand_landmarks.landmark[0].y*height), int(hand_landmarks.landmark[0].x*width)])
hand_color = np.average(colors, axis=0)
print(hand_color)

resultImage = ImageProcessing.DeleteBackground(image, hand_color, 10,50,300, max_area=40)

# ==================== 저장할 경로를 설정해주세용 ==================== #
cv2.imwrite("rock0.png", resultImage)