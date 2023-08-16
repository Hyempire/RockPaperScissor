"""
paper_captures, rock_captures, scissor_captures dir들을 순환하며 이미지 파일들의 배경을 제거하는 코드
"""

import cv2
import mediapipe as mp
import numpy as np
import os
import ImageProcessing

# ===== 파일 이름 설정!!!! 각자 바꿔줘야 하는 부분!! ===== #
your_name = "hyemi"
# ===================================================== #

# ===== Mediapipe, Camera Settings ===== #
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
# Open Hand module
hands = mp_hands.Hands(max_num_hands = 1,
                 min_detection_confidence = 0.5,
                 min_tracking_confidence = 0.5)

# Directories initialize
directory_list = [f'./{your_name}/rock_captures',
                  f'./{your_name}/paper_captures',
                  f'./{your_name}/scissor_captures']
final_dir_list = [f'./{your_name}/rock',
                  f'./{your_name}/paper',
                  f'./{your_name}/scissor']
classes = ['rock', 'paper', 'scissor']
# Initialize lists for confirm
datas = {}


try:
    # 세 개의 디렉토리를 순환
    for idx, directory in enumerate(directory_list):
        images = []

        # 각 이미지 파일의 경로를 저장해서 이미지를 읽어들임
        image_files = os.listdir(directory)
        for j, image_file in enumerate(image_files):

            image_path = f'{directory}/{image_file}'

            # 각 이미지 파일을 엶
            image = cv2.imread(image_path)
            height, width, _ = image.shape

            image.flags.writeable = False

            # Hand Tracking
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

            image.flags.writeable = True

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

            # =========== 인자값들을 바꿔보며 그나마 잘 나오는 값을 넣어주세요 ========== #
            resultImage, mask = ImageProcessing.DeleteBackground(image, hand_color, 20,50,300, max_area=300)

            # 새로운 파일들 저장
            new_path = f'./{your_name}/{classes[idx]}/{classes[idx]}_{j}.png'
            cv2.imwrite(new_path, resultImage)
            print(new_path)

            # 이미지 파일의 개수를 추적하기 위해 리스트에 담아줌
            images.append(image_file)
        datas[final_dir_list[idx]] = images
    
    print("Process completed")
    print(f'rock: {len(datas[final_dir_list[0]])},\npaper: {len(datas[final_dir_list[1]])},\nscissor: {len(datas[final_dir_list[2]])}')

except OSError as e:
    print("Error: ",e)
