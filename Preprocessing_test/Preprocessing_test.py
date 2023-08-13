"""
실시간 영상에서 C를 누르면 손을 캡쳐하고 배경을 제거해서 저장하는 코드
"""

import cv2
import mediapipe as mp
import numpy as np
import ImageProcessing

resultImage = np.zeros((300,200,3), np.uint16)
colors = list()

# ===== Mediapipe, Camera Settings ===== #
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
# Open Hand module
hands = mp_hands.Hands(max_num_hands = 1,
                 min_detection_confidence = 0.5,
                 min_tracking_confidence = 0.5)



# ===== Open Camera ===== #
while cap.isOpened():

    # Read a frame
    success, image = cap.read()
    if not success:
        continue
    height, width, _ = image.shape

    # Convert color channel while flip image to selfie mode
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # Process hand detection
    results = hands.process(image)

    # Convert color channel back to CV2's channel
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # ===== When hand tracking succeeded ===== #
    if results.multi_hand_landmarks:

        # list of each landmark's location
        landmarks = []

        # Traverse every landmark in a hand
        for hand_landmarks in results.multi_hand_landmarks:

            # ===== Make a Bounding Box ===== #
            # Contain each landmark's location
            for i in range(len(hand_landmarks.landmark)):
                landmarks.append([int(hand_landmarks.landmark[i].x * width),
                                 int(hand_landmarks.landmark[i].y * height)])
                # Add every colors
                colors.append(image[int(hand_landmarks.landmark[0].y*height), int(hand_landmarks.landmark[0].x*width)])

            # Straight bounding box
            x, y, w, h = cv2.boundingRect(np.array(landmarks))
            #cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)
            
            # ===== Make 300 * 200 box, on the axis of the center ===== #
            # With the premize that the camera is at the side of a hand
            center = {'x': x+w//2, 'y': y+h//2}
            cv2.circle(image, (center['x'], center['y']), 2, (255,0,0), 1)
            # Calculate a region of interest
            startX = center['x'] - 150
            startY = center['y'] - 100
            endX = center['x'] + 150
            endY = center['y'] + 100
            cv2.rectangle(image, (startX,startY), (endX,endY), (0,255,0), 2)

            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)       # 랜드마크 그림

    # Show frames
    cv2.imshow('WebCam', image)

    # Trigger for capturing
    if cv2.waitKey(1) == ord('c'):
        # Save image
        roi = image[startY:endY, startX:endX]
        cv2.imwrite('captured.png', roi)
        print("Captured")

        # Average 
        hand_color = np.average(colors, axis=0)
        print(hand_color)

        # hand_color = image[int(hand_landmarks.landmark[0].y*height), int(hand_landmarks.landmark[0].x*width)]

        resultImage = ImageProcessing.DeleteBackground(roi, hand_color, 7, 40, 300)
        cv2.imwrite('RealtimeHSV.png', resultImage)

    if cv2.waitKey(1) == 27:
        break

cap.release()


# ===== Image Processing ===== #
# roi = cv2.imread('captured.png')  # for testing with still image
# height, width, _ = roi.shape
# center_color = roi[height//2, width//2]
# print(f"Center color : {center_color}")

# ===== BGR test - Not proper for this case ===== #
# thresB = 50
# thresG = 50
# thresR = 50
# minBGR = np.array([center_color[0] - thresB, center_color[1] - thresG, center_color[2] - thresR])
# maxBGR = np.array([center_color[0] + thresB, center_color[1] + thresG, center_color[2] + thresR])

# maskBGR = cv2.inRange(roi, minBGR, maxBGR)
# cv2.imwrite('BGRmask.png', maskBGR)
# resultBGR = cv2.bitwise_and(roi, roi, mask=maskBGR)

# cv2.imwrite('BGR.png', resultBGR)

# ===== HSV test - narrow range of Hue, wide range of Value===== #
# thresH = 8
# thresS = 30
# thresV = 95
# roi_HSV = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
# color_HSV = cv2.cvtColor( np.uint8([[center_color]] ), cv2.COLOR_BGR2HSV)[0][0]
# print(f"HSV : {color_HSV}")
# # Wider range space expecially for V(value)
# minHSV = np.array([color_HSV[0] - thresH, color_HSV[1] - thresS, color_HSV[2] - thresV])
# maxHSV = np.array([color_HSV[0] + thresH, color_HSV[1] + thresS, color_HSV[2] + thresV])

# # Create a mask
# maskHSV = cv2.inRange(roi_HSV, minHSV, maxHSV)
# cv2.imwrite('HSVmask.png', maskHSV)
# # Bilateral filter 
# maskBlured = cv2.bilateralFilter(maskHSV,10,75,75)    # d : pixel range, sigmaColor/Space

# resultHSV = cv2.bitwise_and(roi_HSV, roi_HSV, mask=maskBlured)
# resultHSV = cv2.cvtColor(resultHSV, cv2.COLOR_HSV2BGR)

# cv2.imwrite('HSV.png', resultHSV)