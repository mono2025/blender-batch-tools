import bpy, math, os

# ---- Settings ----
OUTPUT_DIR = "//turntables/"   # // means relative to the .blend file
FRAMES = 72                     # 72 frames = 5° per frame
CAM_DISTANCE = 6.0
CAM_HEIGHT = 2.0

scene = bpy.context.scene
selected = [o for o in bpy.context.selected_objects if o.type == 'MESH']

# Empty at the origin that the camera orbits around
pivot = bpy.data.objects.new("TT_Pivot", None)
scene.collection.objects.link(pivot)

cam_data = bpy.data.cameras.new("TT_Cam")
cam = bpy.data.objects.new("TT_Cam", cam_data)
scene.collection.objects.link(cam)
cam.location = (0, -CAM_DISTANCE, CAM_HEIGHT)
cam.parent = pivot
track = cam.constraints.new('TRACK_TO')
track.target = pivot
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'
scene.camera = cam

scene.frame_start = 1
scene.frame_end = FRAMES
pivot.rotation_euler = (0, 0, 0)
pivot.keyframe_insert("rotation_euler", index=2, frame=1)
pivot.rotation_euler[2] = math.radians(360 * (FRAMES - 1) / FRAMES)
pivot.keyframe_insert("rotation_euler", index=2, frame=FRAMES)
for fc in pivot.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = 'LINEAR'

for obj in selected:
    # Show only the current object
    for other in selected:
        other.hide_render = (other != obj)
    pivot.location = obj.location
    scene.render.filepath = os.path.join(OUTPUT_DIR, obj.name, "frame_")
    bpy.ops.render.render(animation=True)

for other in selected:
    other.hide_render = False
print("Turntables done.")
