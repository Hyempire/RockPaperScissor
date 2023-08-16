import cv2
import numpy as np

def process_number(num):
    if num < 0:
        return 0
    else:
        return num


def DeleteBackground(roi, center_color, thresH, thresS, thresV, max_area = 0):
    """
    parameters
        roi : image
        center_color : hand color (BGR)
        thresH : 색상 문턱값. 값이 클수록 다양한 색상을 통과시킴
        thresS : 채도 문턱값. 값이 클수록 다양한 채도를 통과시킴
        thresV : 밝기 문턱값. 값이 클수록 다양한 밝기를 통과시킴
        max_area : 노이즈 크기 문턱값. 값이 클수록 큰 크기의 노이즈까지 지워버림
    """
    # roi_HSV = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # color_HSV = cv2.cvtColor( np.uint8([[center_color]] ), cv2.COLOR_BGR2HSV)[0][0]
    # print(f"HSV : {color_HSV}")
    # Wider range space expecially for V(value)
    minHSV = np.array([center_color[0] - thresH, center_color[1] - thresS, center_color[2] - thresV])
    maxHSV = np.array([center_color[0] + thresH, center_color[1] + thresS, center_color[2] + thresV])

    # Create a mask
    maskHSV = cv2.inRange(roi, minHSV, maxHSV)
    mask=maskHSV

    # Morph
    morph = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    # Erosion
    mask = cv2.erode(mask, morph)

    # Delete contours except the biggest one
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    selected_contours = []
    blank_image = np.zeros(mask.shape, np.uint8)
    max_contour = contours[0]

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour
            selected_contours.append(max_contour)

    cv2.fillPoly(blank_image, selected_contours, color = (255,255,255))
    mask = blank_image

    
    # 테두리 확장
    kernel = np.ones((4,4),np.uint8)
    #extrapolate the hand to fill dark spots within
    mask = cv2.dilate(mask,kernel,iterations = 2)
    
    # 빈틈 메꾸기
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    
    
    # # 자잘한 픽셀 없애기
    # mask = cv2.medianBlur(mask, 5) 

    # Masked image
    hand_segmented = cv2.bitwise_and(roi, roi, mask=mask)
    resultBGR = cv2.cvtColor(hand_segmented, cv2.COLOR_HSV2BGR)

    black_pixels = np.all(resultBGR == [0, 0, 0], axis=-1)
    resultBGR[black_pixels] = [20, 160, 20]  # 초록색으로 변경

    return resultBGR, mask