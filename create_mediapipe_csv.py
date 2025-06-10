import cv2
import mediapipe as mp
import csv
import os
from tkinter import filedialog, Tk

# GUI로 영상 파일 선택
Tk().withdraw()
video_path = filedialog.askopenfilename(title="영상 파일 선택", filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
if not video_path:
    print("❌ 영상 파일을 선택하지 않았습니다.")
    exit()

# MediaPipe 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=False)
mp_drawing = mp.solutions.drawing_utils

# 영상 열기
cap = cv2.VideoCapture(video_path)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 결과 저장 준비
output_file = "8.csv"
landmark_names = [l.name.lower() for l in mp_pose.PoseLandmark]

with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['frame', 'joint', 'x', 'y', 'z']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # BGR → RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_world_landmarks:
            for idx, lm in enumerate(results.pose_world_landmarks.landmark):
               if lm.visibility > 0.1:
                writer.writerow({
                    'frame': frame_idx,
                    'joint': landmark_names[idx],
                    'x': lm.x,
                    'y': lm.y,
                    'z': lm.z
                })

        frame_idx += 1

cap.release()
pose.close()
print(f"✅ CSV 저장 완료: {output_file}")
