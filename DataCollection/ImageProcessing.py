import cv2
import numpy as np

def DeleteBackground(roi, center_color, thresH, thresS, thresV, max_area = 50):
    """
    parameters
        roi : image
        center_color : hand color (BGR)
        thresH : 색상 문턱값. 값이 클수록 다양한 색상을 통과시킴
        thresS : 채도 문턱값. 값이 클수록 다양한 채도를 통과시킴
        thresV : 밝기 문턱값. 값이 클수록 다양한 밝기를 통과시킴
        max_area : 노이즈 크기 문턱값. 값이 클수록 큰 크기의 노이즈까지 지워버림
    """
    roi_HSV = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    color_HSV = cv2.cvtColor( np.uint8([[center_color]] ), cv2.COLOR_BGR2HSV)[0][0]
    # print(f"HSV : {color_HSV}")
    # Wider range space expecially for V(value)
    minHSV = np.array([color_HSV[0] - thresH, color_HSV[1] - thresS, color_HSV[2] - thresV])
    maxHSV = np.array([color_HSV[0] + thresH, color_HSV[1] + thresS, color_HSV[2] + thresV])

    # Create a mask
    maskHSV = cv2.inRange(roi_HSV, minHSV, maxHSV)
    mask=maskHSV
    cv2.imwrite('rock_mask.png', mask)

    # Find contours
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
    
    # Gaussian filter
    mask = cv2.GaussianBlur(mask, (5,5), 5)

    # Bilateral filter 
    maskBlured = cv2.bilateralFilter(mask,3,100,75)    # d : pixel range, sigmaColor/Space
    mask=maskBlured
    
    # Morph
    morph = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    # Erosion
    mask = cv2.erode(mask, morph)
    
    

    # cv2.imwrite('RealtimeContouredMask.png', mask)

    # Masked image
    hand_segmented = cv2.bitwise_and(roi_HSV, roi_HSV, mask=mask)
    resultBGR = cv2.cvtColor(hand_segmented, cv2.COLOR_HSV2BGR)

    black_pixels = np.all(resultBGR == [0, 0, 0], axis=-1)
    resultBGR[black_pixels] = [20, 160, 20]  # 초록색으로 변경

    return resultBGR