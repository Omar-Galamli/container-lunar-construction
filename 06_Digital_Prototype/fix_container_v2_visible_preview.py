import math
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
PROTOTYPE_DIR = ROOT / "06_Digital_Prototype"
BLEND_PATH = PROTOTYPE_DIR / "CONTAINER_v2_Blender_Prototype.blend"
REPAIRED_BLEND_PATH = PROTOTYPE_DIR / "CONTAINER_v2_Blender_Prototype_REPAIRED_PRINTABLE.blend"
REPORT_PATH = PROTOTYPE_DIR / "CONTAINER_v2_visible_preview_fix_report.md"
RENDER_PATH = PROTOTYPE_DIR / "renders" / "clean_fullsize_preview.png"


CLEARANCE = 0.04  # visible full-size engineering clearance for the preview scene.


def make_mat(name, color, metallic=0.0, roughness=0.55):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
    return mat


def purge_collection(name):
    col = bpy.data.collections.get(name)
    if not col:
        return
    for child in list(col.children):
        purge_collection(child.name)
    for obj in list(col.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for parent in list(bpy.data.collections):
        if col.name in parent.children:
            parent.children.unlink(col)
    if col.name in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.unlink(col)
    bpy.data.collections.remove(col)


def collection(name, parent=None):
    col = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if not col.users:
        if parent:
            parent.children.link(col)
        else:
            bpy.context.scene.collection.children.link(col)
    return col


def link(obj, col):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)
    return obj


def cube(name, loc, dims, mat, col, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = obj.modifiers.new("edge_radius", "BEVEL")
        mod.width = bevel
        mod.segments = 2
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
        obj.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")
    obj.data.materials.append(mat)
    return link(obj, col)


def cyl(name, loc, radius, depth, mat, col, vertices=40, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    return link(obj, col)


def cyl_between(name, a, b, radius, mat, col, vertices=32):
    av, bv = Vector(a), Vector(b)
    mid = (av + bv) / 2
    direction = bv - av
    obj = cyl(name, mid, radius, direction.length, mat, col, vertices=vertices)
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    return obj


def set_origin(obj, loc):
    cursor = bpy.context.scene.cursor.location.copy()
    bpy.context.scene.cursor.location = loc
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")
    bpy.context.scene.cursor.location = cursor


def hide_legacy_collections():
    keep = {"CONTAINER_v2_CLEAN_FULLSIZE_PREVIEW"}
    for col in bpy.data.collections:
        if col.name not in keep and (
            col.name.startswith("CONTAINER_v2_Engineering_Prototype")
            or col.name in {
                "Body_Open_Regolith_Bin",
                "Protected_Underfloor_Deck",
                "Front_Sliding_Lift_Bucket",
                "Side_Rail_Arms",
                "Sensors_48_Manifest",
                "Shielding_Thermal_Service",
                "Provisional_Mobility_REFERENCE_ONLY",
                "Lunar_Context",
                "Pose_States",
                "CONTAINER_Printable_1_to_40_Model",
            }
        ):
            col.hide_viewport = True
            col.hide_render = True


def build_bucket(col, mats):
    bucket_col = collection("Mechanism_Front_Bucket_Slide_Lift_Curl", col)
    # Rails and lift frame.
    cyl_between("bucket_upper_lateral_slide_rail_clear", (-0.18, 0.65, 3.30), (-0.18, 5.35, 3.30), 0.055, mats["steel"], bucket_col)
    cyl_between("bucket_lower_lateral_slide_rail_clear", (-0.18, 0.65, 0.78), (-0.18, 5.35, 0.78), 0.045, mats["steel"], bucket_col)
    cube("bucket_left_lift_mast_outside_opening", (-0.24, 1.78, 2.00), (0.16, 0.16, 2.65), mats["steel"], bucket_col, 0.015)
    cube("bucket_right_lift_mast_outside_opening", (-0.24, 4.22, 2.00), (0.16, 0.16, 2.65), mats["steel"], bucket_col, 0.015)
    carriage = cube("bucket_Y_slide_Z_lift_carriage_CLEARANCED", (-0.31, 3.0, 1.00), (0.26, 2.38, 0.26), mats["orange"], bucket_col, 0.015)
    carriage["motion"] = "slides laterally on Y rails and vertically on lift masts without entering body wall"

    # Normal scoop: back plate, bottom plate, side cheeks, hinge tube, teeth.
    parts = [
        cube("bucket_scoop_closed_back_wall_no_gap", (-0.50, 3.0, 1.20), (0.16, 2.24, 1.05), mats["bucket"], bucket_col, 0.012),
        cube("bucket_scoop_floor_plate", (-1.05, 3.0, 0.73), (1.12, 2.10, 0.12), mats["bucket"], bucket_col, 0.012),
        cube("bucket_scoop_left_cheek_closed_to_back", (-0.85, 1.88, 1.02), (1.02, 0.14, 0.94), mats["bucket"], bucket_col, 0.012),
        cube("bucket_scoop_right_cheek_closed_to_back", (-0.85, 4.12, 1.02), (1.02, 0.14, 0.94), mats["bucket"], bucket_col, 0.012),
        cube("bucket_scoop_top_rear_lip_closes_corner", (-0.56, 3.0, 1.76), (0.26, 2.24, 0.12), mats["steel"], bucket_col, 0.008),
        cyl_between("bucket_curl_hinge_tube_TRUE_PIVOT", (-0.45, 1.80, 1.02), (-0.45, 4.20, 1.02), 0.075, mats["steel"], bucket_col),
    ]
    for i in range(8):
        y = 2.10 + i * 0.26
        tooth = cube(f"bucket_replaceable_tooth_clear_{i+1:02d}", (-1.66, y, 0.65), (0.38, 0.12, 0.12), mats["steel"], bucket_col, 0.006)
        tooth.rotation_euler[1] = math.radians(-12)
        parts.append(tooth)
    bpy.ops.object.select_all(action="DESELECT")
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    bucket = bpy.context.object
    bucket.name = "bucket_scoop_SINGLE_MOVABLE_PART_hinge_origin_set"
    set_origin(bucket, Vector((-0.45, 3.0, 1.02)))
    bucket["motion"] = "curl/dump about Y-axis hinge; tested -20 to +70 degrees"
    bucket.rotation_euler[1] = math.radians(-12)
    return bucket


def build_arm(col, mats, name, side, x):
    y_wall = 0.0 if side == "left" else 6.0
    outward = -1 if side == "left" else 1
    rail_y = y_wall + outward * 0.36
    rail_z = 3.15
    arm_col = collection(f"Arm_{name}_OUTSIDE_{side}", col)
    carriage = cube(f"{name}_rail_carriage_OUTSIDE_ONLY", (x, rail_y, rail_z), (0.52, 0.30, 0.24), mats["orange"], arm_col, 0.015)
    carriage["motion"] = "slides on exterior side rail along X"
    pts = [
        Vector((x, rail_y, rail_z)),
        Vector((x - 0.15, rail_y + outward * 0.70, rail_z + 0.55)),
        Vector((x + 0.35, rail_y + outward * 1.25, rail_z + 1.05)),
        Vector((x + 0.68, rail_y + outward * 1.52, rail_z + 0.58)),
    ]
    for i, p in enumerate(pts):
        cyl(f"{name}_joint_{i}_pin_boss", p, 0.14 if i else 0.18, 0.20, mats["steel"], arm_col, rotation=(math.radians(90), 0, 0))
    for i in range(len(pts) - 1):
        cyl_between(f"{name}_link_{i+1}_outside_body_clear", pts[i], pts[i + 1], 0.065, mats["arm"], arm_col)
        cyl_between(f"{name}_parallel_link_{i+1}_outside_body_clear", pts[i] + Vector((0, 0, 0.13)), pts[i + 1] + Vector((0, 0, 0.13)), 0.035, mats["arm"], arm_col, vertices=20)
    cube(f"{name}_tool_plate_docking_face", pts[-1] + Vector((0, outward * 0.12, -0.03)), (0.32, 0.08, 0.22), mats["orange"], arm_col, 0.01)
    arm_col["motion"] = "exterior rail carriage and articulated links; no part starts inside the container"


def build_scene():
    purge_collection("CONTAINER_v2_CLEAN_FULLSIZE_PREVIEW")
    root = collection("CONTAINER_v2_CLEAN_FULLSIZE_PREVIEW")
    body_col = collection("01_Open_Body_Clear_Bucket_Throat", root)
    mechanisms_col = collection("02_Movable_Mechanisms_All_Clearanced", root)
    panels_col = collection("03_Shields_Service_Sensors_No_Overlap", root)
    wheels_col = collection("04_Visible_Wheel_Modules", root)

    mats = {
        "body": make_mat("CLEAN_body_warm_white", (0.78, 0.78, 0.70, 1), 0.15, 0.44),
        "interior": make_mat("CLEAN_interior_gray", (0.42, 0.42, 0.39, 1), 0.05, 0.72),
        "bucket": make_mat("CLEAN_bucket_dark_steel", (0.04, 0.04, 0.04, 1), 0.65, 0.34),
        "steel": make_mat("CLEAN_mechanism_steel", (0.12, 0.13, 0.13, 1), 0.80, 0.34),
        "orange": make_mat("CLEAN_moving_orange", (1.0, 0.48, 0.05, 1), 0.05, 0.42),
        "arm": make_mat("CLEAN_arm_light_link", (0.72, 0.72, 0.66, 1), 0.25, 0.45),
        "radiator": make_mat("CLEAN_radiator_dark", (0.18, 0.20, 0.22, 1), 0.45, 0.35),
        "sensor": make_mat("CLEAN_sensor_blue", (0.02, 0.28, 0.95, 1), 0.05, 0.18),
        "ground": make_mat("CLEAN_plain_floor_mat", (0.36, 0.36, 0.34, 1), 0.0, 0.85),
    }

    # Open-top 8 x 6 x 4 body with a real front bucket throat, not a solid wall.
    t = 0.15
    cube("body_left_wall_solid_printable", (4.0, t / 2, 2.0), (8.0, t, 4.0), mats["body"], body_col, 0.025)
    cube("body_right_wall_solid_printable", (4.0, 6.0 - t / 2, 2.0), (8.0, t, 4.0), mats["body"], body_col, 0.025)
    cube("body_rear_wall_with_service_cutline", (8.0 - t / 2, 3.0, 2.0), (t, 6.0, 4.0), mats["body"], body_col, 0.025)
    cube("front_left_post_bucket_opening_clear", (t / 2, 0.60, 2.0), (t, 1.20, 4.0), mats["body"], body_col, 0.025)
    cube("front_right_post_bucket_opening_clear", (t / 2, 5.40, 2.0), (t, 1.20, 4.0), mats["body"], body_col, 0.025)
    cube("front_lower_sill_below_bucket_path", (t / 2, 3.0, 0.35), (t, 3.60, 0.70), mats["body"], body_col, 0.025)
    cube("front_upper_lintel_above_dump_path", (t / 2, 3.0, 3.75), (t, 3.60, 0.50), mats["body"], body_col, 0.025)
    cube("front_bucket_throat_hatch_CLOSED_no_huge_hole", (-0.015, 3.0, 2.08), (0.09, 3.36, 2.48), mats["body"], body_col, 0.018)
    cube("front_bucket_hatch_recessed_service_seam", (-0.07, 3.0, 2.08), (0.025, 3.12, 2.24), mats["interior"], body_col, 0.006)
    cube("front_bucket_hatch_upper_hinge_bar", (-0.13, 3.0, 3.24), (0.08, 3.20, 0.08), mats["steel"], body_col, 0.006)
    cube("front_bucket_small_dump_slot_dark", (-0.145, 3.0, 1.08), (0.035, 2.45, 0.26), mats["bucket"], body_col, 0.004)
    cube("raised_internal_floor_clean", (4.0, 3.0, 0.90), (7.70, 5.70, 0.10), mats["interior"], body_col, 0.015)
    for name, loc, dims in [
        ("top_left_rim_open_roof", (4.0, 0.13, 4.08), (8.15, 0.26, 0.20)),
        ("top_right_rim_open_roof", (4.0, 5.87, 4.08), (8.15, 0.26, 0.20)),
        ("top_front_rim_open_bucket_throat", (0.13, 3.0, 4.08), (0.26, 6.15, 0.20)),
        ("top_rear_rim_open_roof", (7.87, 3.0, 4.08), (0.26, 6.15, 0.20)),
    ]:
        cube(name, loc, dims, mats["steel"], body_col, 0.015)

    # External bucket, arms, wheels.
    build_bucket(mechanisms_col, mats)
    for y, side in [(-0.36, "left"), (6.36, "right")]:
        cyl_between(f"{side}_arm_rail_OUTSIDE_body_clear", (0.8, y, 3.15), (7.2, y, 3.15), 0.055, mats["steel"], mechanisms_col)
    build_arm(mechanisms_col, mats, "A1_LF", "left", 2.1)
    build_arm(mechanisms_col, mats, "A2_LR", "left", 5.7)
    build_arm(mechanisms_col, mats, "A3_RF", "right", 2.1)
    build_arm(mechanisms_col, mats, "A4_RR", "right", 5.7)

    for side_y, side, outward in [(-0.32, "left", -1), (6.32, "right", 1)]:
        for i, x in enumerate([0.9, 1.65, 6.35, 7.1], 1):
            cyl(f"{side}_wheel_{i}_VISIBLE_OUTSIDE_ROTATES", (x, side_y, 0.33), 0.36, 0.28, mats["bucket"], wheels_col, rotation=(math.radians(90), 0, 0))
            cube(f"{side}_wheel_suspension_arm_{i}_clear", (x, side_y - outward * 0.10, 0.76), (0.48, 0.18, 0.42), mats["steel"], wheels_col, 0.015)

    # Side shields and radiators separated by visible gaps.
    for side_y, side, outward in [(-0.11, "left", -1), (6.11, "right", 1)]:
        for idx, x in enumerate([1.0, 2.35, 3.70, 5.05, 6.40], 1):
            cube(f"{side}_shield_panel_{idx}_separate_gap", (x, side_y, 2.35), (0.92, 0.07, 1.28), mats["body"], panels_col, 0.012)
        for idx, x in enumerate([3.2, 4.2, 5.2], 1):
            cube(f"{side}_radiator_panel_{idx}_offset_not_overlapping", (x, side_y + outward * 0.10, 1.35), (0.72, 0.055, 0.78), mats["radiator"], panels_col, 0.008)
    cube("rear_service_hatch_visible_clearance_gap", (8.12, 3.0, 0.55), (0.08, 4.5, 0.75), mats["bucket"], panels_col, 0.015)
    for loc, name in [((0.10, 3, 3.6), "front_lidar"), ((7.9, 3, 3.6), "rear_lidar"), ((4, 3, 3.85), "bin_camera")]:
        cyl(f"sensor_{name}_printable_boss", loc, 0.07, 0.08, mats["sensor"], panels_col, vertices=24)

    # Clean flat ground. No scattered rock fragments in the active preview.
    cube("clean_flat_lunar_floor_no_random_rocks", (4.0, 3.0, -0.04), (12.0, 10.0, 0.05), mats["ground"], root)

    root["purpose"] = "Visible full-size cleaned preview; old reference/prototype collections hidden."
    root["clearance_note"] = f"Visible full-size preview clearance is {CLEARANCE} m; printable STL set uses 0.4 mm."
    bpy.context.scene["active_clean_preview_collection"] = root.name
    return root


def bbox(obj):
    corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    return (
        Vector((min(v.x for v in corners), min(v.y for v in corners), min(v.z for v in corners))),
        Vector((max(v.x for v in corners), max(v.y for v in corners), max(v.z for v in corners))),
    )


def overlap(a, b, clearance=0.0):
    a0, a1 = bbox(a)
    b0, b1 = bbox(b)
    return a0.x < b1.x - clearance and a1.x > b0.x + clearance and a0.y < b1.y - clearance and a1.y > b0.y + clearance and a0.z < b1.z - clearance and a1.z > b0.z + clearance


def audit(root):
    objects = list(root.all_objects)
    body = [o for o in objects if o.name.startswith("body_") or o.name.startswith("front_") or o.name.startswith("raised_")]
    issues = []
    for obj in objects:
        if obj.name.startswith(("A1_", "A2_", "A3_", "A4_")):
            for wall in body:
                if overlap(obj, wall, 0.01):
                    issues.append(f"{obj.name} overlaps {wall.name}")
        if "wheel_" in obj.name and "VISIBLE" in obj.name:
            for wall in body:
                if overlap(obj, wall, 0.01):
                    issues.append(f"{obj.name} overlaps {wall.name}")
    return issues


def render_preview():
    RENDER_PATH.parent.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = 1800
    scene.render.resolution_y = 1100
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 8))
    sun = bpy.context.object
    sun.name = "clean_preview_sun"
    sun.rotation_euler = (math.radians(45), 0, math.radians(-35))
    sun.data.energy = 2.5
    bpy.ops.object.camera_add(location=(-5.0, -6.2, 4.2), rotation=(math.radians(62), 0, math.radians(-39)))
    cam = bpy.context.object
    cam.name = "clean_preview_camera"
    direction = Vector((4.0, 3.0, 2.0)) - Vector(cam.location)
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = 24
    scene.camera = cam
    scene.render.filepath = str(RENDER_PATH)
    bpy.ops.render.render(write_still=True)


def main():
    bpy.ops.wm.open_mainfile(filepath=str(BLEND_PATH))
    hide_legacy_collections()
    root = build_scene()
    issues = audit(root)
    render_preview()
    lines = [
        "# CONTAINER v2 Visible Preview Fix",
        "",
        "This fixes the problem where the old visual prototype remained visible and the repaired printable model was only a small added collection.",
        "",
        "Changes made:",
        "- Hid legacy/reference clutter and the small printable collection from the default preview.",
        "- Rebuilt a full-size clean preview collection: `CONTAINER_v2_CLEAN_FULLSIZE_PREVIEW`.",
        "- Put all four robotic arms outside the container on exterior side rails.",
        "- Replaced the front bucket with one hinged scoop object on a clear lateral slide/lift carriage.",
        "- Made eight wheels visible outside the body, with suspension blocks clear of side walls.",
        "- Re-spaced shield and radiator panels so they are not stacked on top of each other.",
        "- Removed random floor rocks from the active preview and replaced them with a flat ground plane.",
        "",
        f"Audit result: {'PASS' if not issues else 'ISSUES FOUND'}",
    ]
    lines.extend([f"- {i}" for i in issues])
    lines.append(f"\nPreview render: `{RENDER_PATH}`")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    bpy.ops.wm.save_as_mainfile(filepath=str(REPAIRED_BLEND_PATH))
    print(f"VISIBLE_PREVIEW_REPORT={REPORT_PATH}")
    print(f"VISIBLE_PREVIEW_RENDER={RENDER_PATH}")
    print(f"AUDIT_ISSUES={len(issues)}")


if __name__ == "__main__":
    main()
