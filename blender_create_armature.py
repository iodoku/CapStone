import bpy

# Bake + Export !
obj = bpy.context.object

if not obj or not obj.animation_data or not obj.animation_data.action:
    print("❌ 애니메이션 데이터가 없는 오브젝트입니다.")
else:
    action = obj.animation_data.action
    start_frame = int(min(kp.co[0] for fc in action.fcurves for kp in fc.keyframe_points))
    end_frame = int(max(kp.co[0] for fc in action.fcurves for kp in fc.keyframe_points))
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame

    bpy.ops.nla.bake(
        frame_start=start_frame,
        frame_end=end_frame,
        only_selected=True,
        visual_keying=True,
        clear_constraints=True,
        use_current_action=True,
        bake_types={'POSE'}
    )
    
# === 사용자 설정 ===
    bpy.ops.export_scene.fbx(
        filepath="C:/Users/leechaehyeon/Desktop/Motion/fbx1.fbx",
        use_selection=False,
        global_scale=1.0,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        object_types={'ARMATURE'},
        bake_anim=True,
        bake_anim_use_all_actions=False,
        bake_anim_use_nla_strips=False,
        bake_anim_force_startend_keying=True,
        add_leaf_bones=False,
        armature_nodetype='ROOT',
        path_mode='AUTO'
    )

    print("✅ FBX 내보내기 완료")
