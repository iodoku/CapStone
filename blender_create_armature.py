import bpy
import mathutils

# 기존 Armature 삭제
for obj in bpy.data.objects:
    if obj.type == 'ARMATURE':
        bpy.data.objects.remove(obj, do_unlink=True)

# 새 Armature 생성
bpy.ops.object.add(type='ARMATURE', enter_editmode=True)
armature = bpy.context.object
armature.name = "HumanArmature"
armature.show_in_front = True

edit_bones = armature.data.edit_bones

# 관절 위치 샘플
joint_positions = {
    "hips": (0, 0, 0),
    "spine": (0, 0, 0.1),
    "chest": (0, 0, 0.25),
    "neck": (0, 0, 0.4),
    "head": (0, 0, 0.55),
    "left_shoulder": (-0.1, 0, 0.3),
    "left_elbow": (-0.2, 0, 0.25),
    "left_wrist": (-0.3, 0, 0.2),
    "right_shoulder": (0.1, 0, 0.3),
    "right_elbow": (0.2, 0, 0.25),
    "right_wrist": (0.3, 0, 0.2),
    "left_hip": (-0.1, 0, -0.1),
    "left_knee": (-0.1, 0, -0.3),
    "left_ankle": (-0.1, 0, -0.5),
    "right_hip": (0.1, 0, -0.1),
    "right_knee": (0.1, 0, -0.3),
    "right_ankle": (0.1, 0, -0.5),
}

bone_hierarchy = [
    ("hips", "spine"),
    ("spine", "chest"),
    ("chest", "neck"),
    ("neck", "head"),
    ("chest", "left_shoulder"),
    ("left_shoulder", "left_elbow"),
    ("left_elbow", "left_wrist"),
    ("chest", "right_shoulder"),
    ("right_shoulder", "right_elbow"),
    ("right_elbow", "right_wrist"),
    ("hips", "left_hip"),
    ("left_hip", "left_knee"),
    ("left_knee", "left_ankle"),
    ("hips", "right_hip"),
    ("right_hip", "right_knee"),
    ("right_knee", "right_ankle"),
]

# 본 생성
for name in joint_positions:
    bone = edit_bones.new(name)
    head = mathutils.Vector(joint_positions[name])
    tail = head + mathutils.Vector((0, 0.02, 0))  # 작게라도 길이 주기
    bone.head = head
    bone.tail = tail

# 부모 설정 (❗️use_connect=False)
for parent, child in bone_hierarchy:
    if parent in edit_bones and child in edit_bones:
        edit_bones[child].parent = edit_bones[parent]
        edit_bones[child].use_connect = False  # 위치 독립 설정
        

bpy.ops.object.mode_set(mode='OBJECT')
