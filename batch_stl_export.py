import bpy, os

# ---- Settings ----
OUTPUT_DIR = bpy.path.abspath("//stl_export/")
APPLY_MODIFIERS = True

os.makedirs(OUTPUT_DIR, exist_ok=True)
selected = [o for o in bpy.context.selected_objects if o.type == 'MESH']

for obj in selected:
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    path = os.path.join(OUTPUT_DIR, f"{obj.name}.stl")
    bpy.ops.wm.stl_export(
        filepath=path,
        export_selected_objects=True,
        apply_modifiers=APPLY_MODIFIERS,
    )
    print("Exported", path)

print(f"Exported {len(selected)} objects.")
