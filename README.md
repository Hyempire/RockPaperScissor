# RockPaperScissor

## 1. 데이터 전처리

- 데이터셋
    
    https://www.kaggle.com/datasets/drgfreeman/rockpaperscissors?resource=download
    
    300*200px png
    
    'Rock' (726 images), 'Paper' (710 images) and 'Scissors' (752 images)
    
### 1 - 1. Image processing
  1. Hand bounding box → 300*200 이미지
  2. 살색 Segmentation → 배경 제거

<br>

> 코드 파일들 : `Preprocessing_test` dir <br>
> - `Preprocessing_test.py` : 실시간 영상에서 손을 중심으로 300*200짜리 bounding box를 만들고 C를 누르면 roi를 캡쳐하고 배경을 제거해서 저장하는 코드
> - `ImageProcessing.py` : 이미지프로세싱에 필요한 함수들을 넣어 놓은 모듈
>   - `DeleteBackground()` : 이미지를 HSV로 변환한 후 배경을 제거하는 함수
> <br>
> 

### 1 - 2. 데이터 수집 코드 짜기
1. 실시간 영상에서 C를 누르면 300*200 roi를 0.5초마다 총 50번 캡쳐하는 코드
   <br>-> `.\rock_captures` `.\paper_captures` `.\scissor_captures`에 저장
2. 디렉토리 하나를 훑으면서 이미지처리를 하는 코드
   <br>-> `.\rock` `.\paper` `.\scissor`에 저장

> == 데이터 수집 안내 ==
> - 웹캡을 손등을 바라보게 위치시켜주세요
> - 배경이 단색일 필요는 없지만, 밝은 회색, 베이지색, 흰 색은 피해주세요
> - `CaptureImages.py` : 실시간 영상에서 C를 누르면 1초마다 한 번씩 50번 손을 캡쳐하는 코드
>     - ***`your_name`과 `hand_pose`와 `capture_count`를 꼭 바꿔주세요***
>     - ***이 코드를 두 번 돌려서, 100개의 데이터를 수집해주세요***
>     - 50번씩 캡쳐되는 동안 손을 가까이서, 멀리서, 약간 비틀어서 등등 다양하게 찍어주세요
>     - 손가락이 roi box를 벗어날 정도로 너무 카메라에 가까이 가면 오류날 수도 있으니 주의해주세요
>     - roi 박스가 화면 밖을 넘어가면 오류납니다
> - `ImageProcess.py` : './{your_name}/rock_captures', './{your_name}/paper_captures', './{your_name}/scissor_captures' 디렉토리 내의 이미지 파일들의 배경을 제거합니다.
>     - `DeleteBackground()` : 배경을 제거하는 코드... 배경에 따라 잘 나오지 않는 경우도 있으니 인자를 바꾸면 조정해보세요
>     - `ImageProcessing.py` 코드 안에 함수 인자들에 대한 설명을 적어놨습니다.
> - `test.py` : ImageProcess.py 파일을 계속 돌리면서 테스트하기 귀찮다면, 이미지를 하나씩만 넣어서 올바른 인자를 찾아볼 수 있는 코드입니다. 하지만 이미지 하나에서 배경이 잘 제거돼었다고 다른 이미지에서 잘 제거될 거라는 보장은 없..

## 2. 신경망 모델링 + 학습

class 3짜리 분류 문제

## 3. 실시간 영상에 적용

### 3 - 1. Open CV + 파이토치 모델

### 3 - 2. 랜덤으로 가위 바위 보 생성

### 3 - 3. GUI 구성