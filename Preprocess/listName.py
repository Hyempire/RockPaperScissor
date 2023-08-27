"""
바보같이 파일 100개 이름을 똑같이 만들어서 이름에 사람 이름 추가하는 코드
귀찮으니까 그 폴더 안으로 이동해서 이 코드 돌리기
"""

import os

folder_path = "Preprocess/Final_dataset"
files = os.listdir(folder_path)

for i, file_name in enumerate(files):
    old_path = os.path.join(folder_path, file_name)

    num = file_name.split(".")[0]
    pose_name = file_name.split("_")[1].split(".")[0]
    new_file_name = f"{num}_{pose_name}.png"
    new_path = os.path.join(folder_path, new_file_name)

    os.rename(old_path, new_path)
    print(f"Renamed '{file_name}' to '{new_file_name}'")

print(f"Completed {folder_path}")
