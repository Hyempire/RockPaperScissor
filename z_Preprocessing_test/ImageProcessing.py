'''
배경 제거에 필요한 함수를 모아놓음 파일
'''

import cv2
import numpy as np

def DeleteBackground(roi, center_color, thresH, thresS, thresV):
    roi_HSV = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    color_HSV = cv2.cvtColor( np.uint8([[center_color]] ), cv2.COLOR_BGR2HSV)[0][0]
    print(f"HSV : {color_HSV}")
    # Wider range space expecially for V(value)
    minHSV = np.array([color_HSV[0] - thresH, color_HSV[1] - thresS, color_HSV[2] - thresV])
    maxHSV = np.array([color_HSV[0] + thresH, color_HSV[1] + thresS, color_HSV[2] + thresV])

    # Create a mask
    maskHSV = cv2.inRange(roi_HSV, minHSV, maxHSV)
    mask=maskHSV
    # cv2.imwrite('RealtimeHSVmask.png', maskHSV)
    # Bilateral filter 
    maskBlured = cv2.bilateralFilter(mask,20,75,75)    # d : pixel range, sigmaColor/Space
    mask=maskBlured
    # Morph
    morph = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
    maskMorph = cv2.erode(mask, morph)
    mask = maskMorph
    #cv2.imwrite('RealtimeHSVmask.png', maskMorph)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    selected_contours = []
    max_area = 10
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

    cv2.imwrite('RealtimeContouredMask.png', mask)

    # Masked image
    resultHSV = cv2.bitwise_and(roi_HSV, roi_HSV, mask=blank_image)
    resultHSV = cv2.cvtColor(resultHSV, cv2.COLOR_HSV2BGR)

    return resultHSV
