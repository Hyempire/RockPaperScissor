# organize imports
import cv2
import imutils
import numpy as np
import mediapipe as mp


def process_number(num):
    if num < 0:
        return 0
    else:
        return num
    

# ===== Mediapipe, Camera Settings ===== #
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
# Open Hand module
hands = mp_hands.Hands(max_num_hands = 1,
                 min_detection_confidence = 0.5,
                 min_tracking_confidence = 0.5)

image = cv2.imread("SegmentationTest\hyemi_paper_92.png")
height, width, _ = image.shape
roi = image.copy()
kernel = np.ones((3,3),np.uint8)

# Hand Tracking
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = hands.process(image)
image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

# handtracking이 성공하면 각 landmark의 컬러값을 평균냄
if results.multi_hand_landmarks is not None:
    # Find hand color
    for hand_landmarks in results.multi_hand_landmarks:
        if results.multi_hand_landmarks:
            colors = []
            for i in range(len(hand_landmarks.landmark)):
                colors.append(image[int(hand_landmarks.landmark[0].y*height), int(hand_landmarks.landmark[0].x*width)])
    hand_color = np.average(colors, axis=0)
    print(f"landmarks color {hand_color}")
else:
    hand_color = image[height//2, width//2]
    print(f"center color {hand_color}")


# define range of skin color in HSV
# lower_skin = np.array([0, 20, 70], dtype=np.uint8)
# upper_skin = np.array([20, 255, 255], dtype=np.uint8)
lower_skin = np.array([process_number(hand_color[0]-10), process_number(hand_color[1]-200), process_number(hand_color[2]-200)], dtype=np.uint8)
upper_skin = np.array([hand_color[0]+20, hand_color[1]+200, hand_color[2]+200], dtype=np.uint8)

#extract skin colur imagw  
mask = cv2.inRange(image, lower_skin, upper_skin)

#extrapolate the hand to fill dark spots within
mask = cv2.dilate(mask,kernel,iterations = 4)

#blur the image
mask = cv2.GaussianBlur(mask,(5,5),100) 

#find contours
contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cv2.imwrite("SegmentationTest/mask.png", mask)

