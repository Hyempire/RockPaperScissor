"""
바보같이 파일 100개 이름을 똑같이 만들어서 이름에 사람 이름 추가하는 코드
귀찮으니까 그 폴더 안으로 이동해서 이 코드 돌리기
"""

import os

pose_name = "rock"
folder_path = "Preprocess/Dataset_bgX_flipO/rock"
files = os.listdir(folder_path)

for i, file_name in enumerate(files):
    old_path = os.path.join(folder_path, file_name)
    
    new_file_name = f"{pose_name}_{i}.png"
    new_path = os.path.join(folder_path, new_file_name)
    
    os.rename(old_path, new_path)
    print(f"Renamed '{file_name}' to '{new_file_name}'")

print(f"Completed {folder_path}")
