# 🦴 Motion Capture to FBX using MediaPipe & Blender

이 프로젝트는 영상에서 사람의 움직임을 MediaPipe로 추출한 후, Blender에서 사람형 뼈대(Armature)에 애니메이션을 적용하고 FBX 포맷으로 내보내는 자동화 파이프라인입니다.

<br>

## 📁 프로젝트 구조

```
├── create_mediapipe_csv.py         # 영상에서 관절 좌표 추출 (MediaPipe 사용)
├── blender_create_armature.py      # Blender에서 사람형 뼈대 생성
├── blender_set_animation_bone.py   # CSV 데이터를 이용해 뼈대에 애니메이션 적용
├── blender_change_fbx.py           # 애니메이션 베이크 후 FBX 파일로 내보내기
```

<br>

## 🚀 전체 실행 흐름

1. **MediaPipe로 관절 좌표 추출**
   - 영상 파일을 입력하면 3D 관절 위치가 CSV로 저장됨
2. **Blender에서 Armature 생성**
   - 사람 형태의 본 구조를 자동 생성
3. **CSV 데이터를 바탕으로 애니메이션 적용**
   - 각 프레임의 관절 위치를 본에 자동 적용
4. **FBX로 내보내기**
   - 애니메이션을 베이크하여 외부 툴에서 활용 가능

<br>


## 📦 요구사항

- Python 
- OpenCV 
- MediaPipe  
- Blender  


## 🧩 파일 설명

### 1️⃣ `create_mediapipe_csv.py`  
MediaPipe를 사용해 영상 속 인물의 관절 위치를 프레임 단위로 추출하고 `CSV`로 저장합니다.

- GUI로 영상 선택 → 프레임별 관절 추출 → `.csv` 생성


### 2️⃣ `blender_create_armature.py`  
사람형 Armature(뼈대)를 Blender에서 자동 생성합니다.

- 본 위치는 미리 정의된 좌표 사용  
- 본 계층 구조 자동 설정 (`hips → spine → chest → neck → head` 등)  
- MediaPipe 구조와 유사하게 설계되어 데이터 적용이 쉬움


### 3️⃣ `blender_set_animation_bone.py`  
MediaPipe CSV 데이터를 기반으로 각 본(Bone)에 애니메이션을 적용합니다.

- Empty 오브젝트를 생성하고 관절 위치를 키프레임으로 설정  
- 본에 `Copy Transforms` 제약을 걸어 Empty를 따라 움직이게 만듦  
- 상대 좌표로 변환하여 자연스러운 동작 구현  


### 4️⃣ `blender_change_fbx.py`  
Blender의 애니메이션을 베이크한 후 `.fbx` 포맷으로 저장합니다.

- 시작/끝 프레임 자동 탐지  
- 시각적으로 보이는 움직임을 키프레임으로 고정 (bake)  
- `.fbx`로 내보내 Unity, Unreal 등에서 사용 가능


## 📷 예시 흐름도

🎥 영상 (.mp4)
   │
   ▼
📄 create_mediapipe_csv.py → 관절 데이터 추출 → .csv 파일 생성
   │
   ▼
🦴 blender_create_armature.py → 사람형 뼈대 생성
   │
   ▼
🏃 blender_set_animation_bone.py → 애니메이션 적용
   │
   ▼
📦 blender_change_fbx.py → .fbx 파일로 저장


## 💡 기대 효과

- 비용 절감, 높은 접근성, 자동화에 의한 생산성 향상  
- 게임, 교육, VR/AR, 애니메이션, AI 학습 데이터 등 다양한 분야에 활용 가능
- 추출부터 적용까지 수작업 없이 진행되는 완전 자동화 파이프라인 구축


## 👥 팀원

- 이채현 (대표학생)  
- 장동하  
- 장지환  
