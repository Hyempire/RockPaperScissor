"""
실시간 영상에서 C를 누르면 0.5초마다 한 번씩 손을 캡쳐하는 코드
"""

import cv2
import mediapipe as mp
import numpy as np
import os
import time

# ===== 파일 이름 설정!!!! 각자 바꿔줘야 하는 부분!! ===== #
your_name = "hyemi3"     # 이름
hand_pose = "scissor"     # rock, paper, scissor
capture_count = 1      # 첫 번째 실행 땐 1, 두 번째 실행 땐 51로 고쳐주세요
# ===================================================== #

if not os.path.exists(f'./{your_name}'):
    os.mkdir(f'./{your_name}')
    os.mkdir(f'./{your_name}/paper_captures')
    os.mkdir(f'./{your_name}/paper')
    os.mkdir(f'./{your_name}/rock_captures')
    os.mkdir(f'./{your_name}/rock')
    os.mkdir(f'./{your_name}/scissor_captures')
    os.mkdir(f'./{your_name}/scissor')

collect_mode = False
capture_end = capture_count + 49

# ===== Mediapipe, Camera Settings ===== #
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
# Open Hand module
hands = mp_hands.Hands(max_num_hands = 1,   # 손은 한 개만 감지하게 함
                 min_detection_confidence = 0.5,
                 min_tracking_confidence = 0.5)

try:
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

                # Straight bounding box
                x, y, w, h = cv2.boundingRect(np.array(landmarks))
                #cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)
                
                # ===== Make 300 * 200 box, on the axis of the center ===== #
                # With the premize that the camera is at the side of a hand
                center = {'x': x+w//2, 'y': y+h//2}
                # cv2.circle(image, (center['x'], center['y']), 2, (255,0,0), 1)
                # Calculate a region of interest
                startX = center['x'] - 150
                startY = center['y'] - 100
                endX = center['x'] + 150
                endY = center['y'] + 100
                cv2.rectangle(image, (startX,startY), (endX,endY), (0,255,0), 2)

                # 랜드마크 그리기 - 데이터 수집할 땐 주석처리해야 함
                # mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Show frames
        cv2.imshow('WebCam', image)

        # Trigger for capturing
        if cv2.waitKey(1) == ord('c'):
            collect_mode = True

        # 데이터 수집 모드 발동!
        if collect_mode == True:

            if capture_count <= capture_end:
                # Save image
                roi = image[startY:endY, startX:endX]

                # Create file path
                file_path = f"./{your_name}/{hand_pose}_captures/{your_name}_{hand_pose}_{capture_count}.png"
                capture_count += 1
                # Save an image
                cv2.imwrite(file_path, roi)
                print(f"Captured {file_path}")

                time.sleep(1)   # 1초마다 캡쳐

            else:
                collect_mode = False
                print("Data Collect mode off")

        if cv2.waitKey(1) == 27:
            break
        
except Exception as e:
    print("Exception occurred:", e)
finally:
    cap.release()
