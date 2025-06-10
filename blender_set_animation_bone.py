import bpy
import mathutils
import csv
from collections import defaultdict

# === 사용자 설정 ===
csv_path = "C:/Users/wlghk/OneDrive/Desktop/Motion/csv/1.csv"
scale_factor = 300.0
armature_name = "HumanArmature"

# === 기존 Armature 및 Empty 제거 ===
for obj in bpy.data.objects:
    if obj.type == 'ARMATURE' or obj.name.startswith("CTRL_"):
        bpy.data.objects.remove(obj, do_unlink=True)

# === Armature 생성 ===
bpy.ops.object.add(type='ARMATURE', enter_editmode=True)
armature = bpy.context.object
armature.name = armature_name
armature.show_in_front = True
edit_bones = armature.data.edit_bones
for obj in bpy.context.selected_objects:
    obj.select_set(False)
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='EDIT')

ik_bone = armature.pose.bones.get("left_wrist")
if ik_bone:
    ik_constraint = ik_bone.constraints.new(type='IK')
    ik_constraint.target = bpy.data.objects.get("IK_Target_Left_Hand")
    ik_constraint.chain_count = 2  # elbow까지 포함

# === 본 위치 설정 ===
joint_positions = {
    'nose': (0, 0, 0.3), 'left_eye_inner': (-0.03, 0, 0.65), 'left_eye': (-0.04, 0, 0.66),
    'left_eye_outer': (-0.05, 0, 0.65), 'right_eye_inner': (0.03, 0, 0.65), 'right_eye': (0.04, 0, 0.66),
    'right_eye_outer': (0.05, 0, 0.65), 'left_ear': (-0.08, 0, 0.6), 'right_ear': (0.08, 0, 0.6),
    'mouth_left': (-0.02, 0, 0.58), 'mouth_right': (0.02, 0, 0.58),
    'left_shoulder': (-0.15, 0, 0.5), 'right_shoulder': (0.15, 0, 0.5),
    'left_elbow': (-0.25, 0, 0.4), 'right_elbow': (0.25, 0, 0.4),
    'left_wrist': (-0.35, 0, 0.3), 'right_wrist': (0.35, 0, 0.3),
    'left_pinky': (-0.38, 0, 0.28), 'right_pinky': (0.38, 0, 0.28),
    'left_index': (-0.37, 0, 0.29), 'right_index': (0.37, 0, 0.29),
    'left_thumb': (-0.36, 0, 0.31), 'right_thumb': (0.36, 0, 0.31),
    'left_hip': (-0.12, 0, 0.2), 'right_hip': (0.12, 0, 0.2),
    'left_knee': (-0.12, 0, 0.05), 'right_knee': (0.12, 0, 0.05),
    'left_ankle': (-0.12, 0, -0.1), 'right_ankle': (0.12, 0, -0.1),
    'left_heel': (-0.13, -0.01, -0.1), 'right_heel': (0.13, -0.01, -0.1),
    'left_foot_index': (-0.12, 0.02, -0.1), 'right_foot_index': (0.12, 0.02, -0.1),
}

bone_hierarchy = [
    ("left_hip", "left_knee"), ("left_knee", "left_ankle"), ("left_ankle", "left_heel"), ("left_ankle", "left_foot_index"),
    ("right_hip", "right_knee"), ("right_knee", "right_ankle"), ("right_ankle", "right_heel"), ("right_ankle", "right_foot_index"),
    ("left_shoulder", "left_elbow"), ("left_elbow", "left_wrist"), ("left_wrist", "left_thumb"),
    ("left_wrist", "left_index"), ("left_wrist", "left_pinky"),
    ("right_shoulder", "right_elbow"), ("right_elbow", "right_wrist"), ("right_wrist", "right_thumb"),
    ("right_wrist", "right_index"), ("right_wrist", "right_pinky"),
    ("nose", "left_eye_inner"), ("left_eye_inner", "left_eye"), ("left_eye", "left_eye_outer"),
    ("nose", "right_eye_inner"), ("right_eye_inner", "right_eye"), ("right_eye", "right_eye_outer"),
    ("left_eye_outer", "left_ear"), ("right_eye_outer", "right_ear"),
    ("nose", "mouth_left"), ("nose", "mouth_right"),
    ("nose", "left_shoulder"), ("nose", "right_shoulder"),
    ("nose", "left_hip"), ("nose", "right_hip")
]

# === 본 생성 및 연결 ===
bones_temp = {}
for name, head_pos in joint_positions.items():
    bone = edit_bones.new(name)
    bone.head = mathutils.Vector(head_pos)
    # 기본 tail 방향 설정 (눈에 보이게)
    bone.tail = bone.head + mathutils.Vector((0, 0.1, 0))
    bones_temp[name] = bone

for parent, child in bone_hierarchy:
    if parent in bones_temp and child in bones_temp:
        parent_bone = bones_temp[parent]
        child_bone = bones_temp[child]
        parent_bone.tail = child_bone.head
        child_bone.parent = parent_bone
        child_bone.use_connect = False

bpy.ops.object.mode_set(mode='OBJECT')

# === CSV 불러오기 ===
frame_data = defaultdict(dict)
with open(csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        frame = int(row['frame'])
        joint = row['joint'].lower()
        x, y, z = float(row['x']), float(row['y']), float(row['z'])
        frame_data[frame][joint] = (x, y, z)

# === Empty → 본에 COPY_TRANSFORMS 연결 ===
empties = {}
for joint in frame_data[0].keys():
    bpy.ops.object.empty_add(type='SPHERE', radius=0.01, location=(0, 0, 0))
    empty = bpy.context.object
    empty.name = f"CTRL_{joint}"
    empties[joint] = empty

    try:
        bone = armature.pose.bones[joint]
        constraint = bone.constraints.new(type='COPY_TRANSFORMS')
        constraint.target = empty
    except KeyError:
        print(f"⚠️ 본 '{joint}' 없음 → Empty만 생성됨")

# === 키프레임 애니메이션 적용 ===
for frame, joints in frame_data.items():
    bpy.context.scene.frame_set(frame)
    origin = None
    if 'left_hip' in joints and 'right_hip' in joints:
        origin = [(joints['left_hip'][i] + joints['right_hip'][i]) / 2 for i in range(3)]
    elif 'nose' in joints:
        origin = joints['nose']
    else:
        continue

    for joint, pos in joints.items():
        if joint not in empties or origin is None:
            continue
        rel_x = (pos[0] - origin[0]) * scale_factor
        rel_y = (pos[1] - origin[1]) * scale_factor
        rel_z = -(pos[2] - origin[2]) * scale_factor

        empties[joint].location = mathutils.Vector((rel_x, rel_y, rel_z))
        empties[joint].keyframe_insert(data_path="location", frame=frame)

# === 타임라인 범위 설정 ===
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = max(frame_data.keys())

print("✅ MediaPipe CSV 기반 뼈대 애니메이션 적용 완료")
