"""
파일들 복사해서 반전하기
"""

import os
import cv2

folder_path = "Preprocess/Dataset_bgX_flipO/rock"
files = os.listdir(folder_path)

for i, file_name in enumerate(files):
    image_path = os.path.join(folder_path, file_name)
    
    image = cv2.imread(image_path)
    image = cv2.flip(image, 1)
    
    new_file_name = "flipped_" + file_name
    new_file_path = os.path.join(folder_path, new_file_name)
    
    cv2.imwrite(new_file_path, image)

print(f"Completed {folder_path} ---- {i+1} files")
