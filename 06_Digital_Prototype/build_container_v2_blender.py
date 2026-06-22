import math
import os
import random
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
BLEND_PATH = ROOT / "06_Digital_Prototype" / "CONTAINER_v2_Blender_Prototype.blend"
RENDER_DIR = ROOT / "06_Digital_Prototype" / "renders"
LOG_PATH = ROOT / "06_Digital_Prototype" / "CONTAINER_v2_Blender_Prototype_build.log"


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for block in (
        bpy.data.meshes,
        bpy.data.materials,
        bpy.data.cameras,
        bpy.data.lights,
        bpy.data.curves,
    ):
        for item in list(block):
            if item.users == 0:
                block.remove(item)


def make_mat(name, color, metallic=0.0, roughness=0.55):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def collection(name, parent=None):
    col = bpy.data.collections.new(name)
    if parent:
        parent.children.link(col)
    else:
        bpy.context.scene.collection.children.link(col)
    return col


def link_to_collection(obj, col):
    for existing in list(obj.users_collection):
        existing.objects.unlink(obj)
    col.objects.link(obj)
    return obj


def cube_obj(name, loc, scale, mat, col):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    link_to_collection(obj, col)
    return obj


def cyl_between(name, start, end, radius, mat, col, vertices=24):
    start_v = Vector(start)
    end_v = Vector(end)
    mid = (start_v + end_v) * 0.5
    direction = end_v - start_v
    length = direction.length
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=length, location=mid)
    obj = bpy.context.object
    obj.name = name
    quat = direction.to_track_quat("Z", "Y")
    obj.rotation_euler = quat.to_euler()
    if mat:
        obj.data.materials.append(mat)
    link_to_collection(obj, col)
    return obj


def sphere_obj(name, loc, radius, mat, col, segments=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=8, radius=radius, location=loc)
    obj = bpy.context.object
    obj.name = name
    if mat:
        obj.data.materials.append(mat)
    link_to_collection(obj, col)
    return obj


def cone_obj(name, loc, radius1, depth, mat, col, vertices=18, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius1, radius2=0.0, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    if mat:
        obj.data.materials.append(mat)
    link_to_collection(obj, col)
    return obj


def add_label(name, text, loc, size, col, mat=None, rot=(math.radians(65), 0, math.radians(45))):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    obj.data.body = text
    obj.data.align_x = "CENTER"
    obj.data.align_y = "CENTER"
    obj.data.size = size
    if mat:
        obj.data.materials.append(mat)
    link_to_collection(obj, col)
    return obj


def build_bucket(col, mat_dark, mat_metal, prefix, center_y, hinge_z, tilt_deg, visible=True):
    bucket_col = collection(prefix, col)
    for obj in [
        cube_obj(f"{prefix}_curved_shell_proxy", (-0.75, center_y, hinge_z - 0.28), (1.10, 2.00, 0.12), mat_dark, bucket_col),
        cube_obj(f"{prefix}_back_plate", (-0.30, center_y, hinge_z + 0.10), (0.12, 2.00, 0.88), mat_dark, bucket_col),
        cube_obj(f"{prefix}_left_cheek", (-0.75, center_y - 1.05, hinge_z + 0.02), (1.05, 0.10, 0.88), mat_dark, bucket_col),
        cube_obj(f"{prefix}_right_cheek", (-0.75, center_y + 1.05, hinge_z + 0.02), (1.05, 0.10, 0.88), mat_dark, bucket_col),
        cyl_between(f"{prefix}_hinge_tube", (-0.28, center_y - 1.10, hinge_z), (-0.28, center_y + 1.10, hinge_z), 0.07, mat_metal, bucket_col),
    ]:
        obj.rotation_euler[1] = math.radians(tilt_deg)
    for i in range(8):
        y = center_y - 0.875 + i * 0.25
        tooth = cone_obj(f"{prefix}_replaceable_tooth_{i+1:02d}", (-1.34, y, hinge_z - 0.42), 0.075, 0.35, mat_metal, bucket_col, vertices=4, rot=(0, math.radians(90 + tilt_deg), 0))
        tooth.scale.y = 0.42
    bucket_col.hide_viewport = not visible
    bucket_col.hide_render = not visible
    return bucket_col


def build_arm(col, mats, name, shoulder, points):
    arm_col = collection(name, col)
    joint_mat, link_mat, tool_mat = mats
    pts = [shoulder] + points
    for idx, point in enumerate(pts):
        sphere_obj(f"{name}_joint_{idx}", point, 0.13 if idx else 0.18, joint_mat, arm_col)
    for idx in range(len(pts) - 1):
        cyl_between(f"{name}_link_{idx+1}", pts[idx], pts[idx + 1], 0.07, link_mat, arm_col)
        cyl_between(f"{name}_parallel_link_{idx+1}", (pts[idx][0], pts[idx][1], pts[idx][2] + 0.12), (pts[idx + 1][0], pts[idx + 1][1], pts[idx + 1][2] + 0.12), 0.035, link_mat, arm_col, vertices=16)
    end = pts[-1]
    cube_obj(f"{name}_universal_tool_plate", end, (0.34, 0.08, 0.22), tool_mat, arm_col)
    sphere_obj(f"{name}_docking_hand_coupler", (end[0], end[1], end[2] - 0.18), 0.08, tool_mat, arm_col)
    return arm_col


def sensor_marker(sensor_id, sensor_type, loc, col, mats):
    mat = mats["camera"] if "camera" in sensor_type else mats["lidar"] if "LiDAR" in sensor_type or "radar" in sensor_type else mats["sensor"]
    radius = 0.055 if loc[2] > 1.0 else 0.045
    sphere_obj(f"{sensor_id}_{sensor_type.replace('/', '_').replace(' ', '_')}", loc, radius, mat, col, segments=12)


def camera_rotation_toward(loc, target):
    direction = Vector(target) - Vector(loc)
    return direction.to_track_quat("-Z", "Y").to_euler()


def render_camera(name, loc, target, lens, ortho=False, ortho_scale=10.0):
    bpy.ops.object.camera_add(location=loc, rotation=camera_rotation_toward(loc, target))
    cam = bpy.context.object
    cam.name = name
    cam.data.lens = lens
    if ortho:
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = ortho_scale
    bpy.context.scene.camera = cam
    bpy.context.scene.render.filepath = str(RENDER_DIR / f"{name}.png")
    bpy.ops.render.render(write_still=True)
    return cam


def main():
    random.seed(7)
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    clear_scene()

    scene = bpy.context.scene
    scene.name = "CONTAINER_v2_Engineering_Prototype"
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    for engine in ("BLENDER_WORKBENCH", "BLENDER_EEVEE_NEXT", "CYCLES"):
        try:
            scene.render.engine = engine
            break
        except TypeError:
            continue
    if scene.render.engine == "CYCLES":
        scene.cycles.samples = 16
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 1000
    scene.view_settings.view_transform = "Filmic"
    scene.view_settings.look = "Medium High Contrast"

    mats = {
        "body": make_mat("mat_warm_white_shielded_aluminum", (0.78, 0.78, 0.72, 1), 0.2, 0.42),
        "inner": make_mat("mat_bin_interior_scuffed_gray", (0.44, 0.43, 0.39, 1), 0.15, 0.76),
        "dark": make_mat("mat_bucket_blackened_steel", (0.035, 0.035, 0.032, 1), 0.75, 0.36),
        "metal": make_mat("mat_dark_mechanical_metal", (0.12, 0.13, 0.13, 1), 0.85, 0.34),
        "radiator": make_mat("mat_exposed_louvered_radiator", (0.20, 0.22, 0.23, 1), 0.5, 0.24),
        "orange": make_mat("mat_engineering_orange_accents", (1.0, 0.48, 0.05, 1), 0.1, 0.4),
        "sensor": make_mat("mat_sensor_blue", (0.05, 0.24, 0.85, 1), 0.2, 0.22),
        "camera": make_mat("mat_camera_green_glass", (0.02, 0.75, 0.36, 1), 0.0, 0.1),
        "lidar": make_mat("mat_lidar_cyan_glass", (0.0, 0.78, 0.95, 1), 0.0, 0.08),
        "regolith": make_mat("mat_lunar_regolith", (0.42, 0.41, 0.38, 1), 0.0, 0.93),
        "label": make_mat("mat_black_label_text", (0.01, 0.01, 0.01, 1), 0.0, 0.5),
    }

    root_col = collection("CONTAINER_v2_Engineering_Prototype")
    body_col = collection("Body_Open_Regolith_Bin", root_col)
    deck_col = collection("Protected_Underfloor_Deck", root_col)
    bucket_col = collection("Front_Sliding_Lift_Bucket", root_col)
    arms_col = collection("Side_Rail_Arms", root_col)
    sensors_col = collection("Sensors_48_Manifest", root_col)
    shield_col = collection("Shielding_Thermal_Service", root_col)
    mobility_col = collection("Provisional_Mobility_REFERENCE_ONLY", root_col)
    lunar_col = collection("Lunar_Context", root_col)
    pose_col = collection("Pose_States", root_col)

    # Body: datum is front-left-bottom, x=front-to-rear, y=left-to-right, z=up.
    t = 0.15
    cube_obj("fixed_body_left_wall_8m", (4.0, t / 2, 2.0), (8.0, t, 4.0), mats["body"], body_col)
    cube_obj("fixed_body_right_wall_8m", (4.0, 6.0 - t / 2, 2.0), (8.0, t, 4.0), mats["body"], body_col)
    cube_obj("fixed_body_front_wall_bucket_opening", (t / 2, 3.0, 2.0), (t, 6.0, 4.0), mats["body"], body_col)
    cube_obj("fixed_body_rear_service_wall", (8.0 - t / 2, 3.0, 2.0), (t, 6.0, 4.0), mats["body"], body_col)
    cube_obj("raised_internal_floor_Z0900", (4.0, 3.0, 0.90), (7.70, 5.70, 0.08), mats["inner"], body_col)
    cube_obj("open_regolith_bay_shadow_mass_proxy", (4.0, 3.0, 1.55), (6.6, 4.8, 0.12), mats["regolith"], body_col)
    for name, loc, scale in [
        ("reinforced_top_rim_left", (4.0, 0.13, 4.05), (8.15, 0.26, 0.20)),
        ("reinforced_top_rim_right", (4.0, 5.87, 4.05), (8.15, 0.26, 0.20)),
        ("reinforced_top_rim_front", (0.13, 3.0, 4.05), (0.26, 6.15, 0.20)),
        ("reinforced_top_rim_rear", (7.87, 3.0, 4.05), (0.26, 6.15, 0.20)),
    ]:
        cube_obj(name, loc, scale, mats["metal"], body_col)

    # Equipment deck and rear service access.
    cube_obj("rear_service_hatch_Y0600_Y5400_Z0150_Z0850", (8.09, 3.0, 0.50), (0.08, 4.8, 0.70), mats["dark"], deck_col)
    for i, y in enumerate([1.05, 2.15, 3.85, 4.95], 1):
        cube_obj(f"slide_out_battery_tray_{i}", (5.4, y, 0.42), (2.1, 0.50, 0.34), mats["metal"], deck_col)
    cube_obj("rear_avionics_control_bay_X6600_X7900", (7.2, 2.15, 0.52), (1.05, 0.72, 0.42), mats["orange"], deck_col)
    cube_obj("rear_power_distribution_bay", (7.2, 3.85, 0.52), (1.05, 0.72, 0.42), mats["orange"], deck_col)
    for y in [0.42, 5.58]:
        cyl_between("cooling_manifold_underfloor_side", (1.0, y, 0.62), (7.65, y, 0.62), 0.045, mats["lidar"], deck_col)

    # Bucket system.
    cube_obj("front_cross_slide_rail_Y0300_Y5700", (-0.15, 3.0, 3.35), (0.12, 5.4, 0.12), mats["metal"], bucket_col)
    cube_obj("front_lower_cross_slide_rail", (-0.15, 3.0, 0.72), (0.12, 5.4, 0.10), mats["metal"], bucket_col)
    cube_obj("vertical_lift_mast_left", (-0.18, 2.03, 1.95), (0.16, 0.14, 2.65), mats["metal"], bucket_col)
    cube_obj("vertical_lift_mast_right", (-0.18, 3.97, 1.95), (0.16, 0.14, 2.65), mats["metal"], bucket_col)
    cube_obj("bucket_lift_carriage_centerline_Y3000", (-0.24, 3.0, 0.95), (0.24, 2.26, 0.22), mats["orange"], bucket_col)
    build_bucket(bucket_col, mats["dark"], mats["metal"], "Bucket_Home_Low_Scoop", 3.0, 0.95, -18, visible=True)
    build_bucket(pose_col, mats["dark"], mats["metal"], "Bucket_Raised_Dump", 3.0, 3.30, 70, visible=False)

    # Shield/radiator panels.
    for side_y, side_name in [(0.0, "left"), (6.0, "right")]:
        for idx, x in enumerate([1.2, 2.6, 4.0, 5.4, 6.8], 1):
            cube_obj(f"{side_name}_removable_shield_panel_{idx}", (x, side_y + (-0.045 if side_y == 0.0 else 0.045), 2.05), (1.0, 0.08, 1.45), mats["body"], shield_col)
        for idx, x in enumerate([3.2, 4.2, 5.2], 1):
            panel = cube_obj(f"{side_name}_exposed_louvered_radiator_{idx}", (x, side_y + (-0.09 if side_y == 0.0 else 0.09), 1.55), (0.78, 0.06, 0.86), mats["radiator"], shield_col)
            for stripe in range(5):
                cube_obj(f"{side_name}_radiator_{idx}_louver_{stripe+1}", (x, side_y + (-0.13 if side_y == 0.0 else 0.13), 1.22 + stripe * 0.15), (0.70, 0.035, 0.025), mats["metal"], shield_col)

    # Side rails and arms.
    for y, side in [(-0.25, "left"), (6.25, "right")]:
        cyl_between(f"{side}_arm_rail_X0800_X7200_Z3150", (0.8, y, 3.15), (7.2, y, 3.15), 0.055, mats["metal"], arms_col)
        cube_obj(f"{side}_dust_cover_for_arm_rail", (4.0, y, 3.00), (6.4, 0.12, 0.08), mats["dark"], arms_col)

    home_shoulders = {
        "A1_LF": (2.2, -0.25, 3.15),
        "A2_LR": (5.8, -0.25, 3.15),
        "A3_RF": (2.2, 6.25, 3.15),
        "A4_RR": (5.8, 6.25, 3.15),
    }
    home_points = {
        "A1_LF": [(2.0, -1.0, 3.75), (2.6, -1.55, 4.55), (2.8, -1.85, 4.15)],
        "A2_LR": [(5.5, 0.45, 3.85), (5.2, 1.35, 4.45), (4.7, 1.65, 3.95)],
        "A3_RF": [(2.0, 7.0, 3.75), (2.6, 7.55, 4.55), (2.8, 7.85, 4.15)],
        "A4_RR": [(5.5, 5.55, 3.85), (5.2, 4.65, 4.45), (4.7, 4.35, 3.95)],
    }
    for name, shoulder in home_shoulders.items():
        cube_obj(f"{name}_rail_carriage", shoulder, (0.48, 0.36, 0.22), mats["orange"], arms_col)
        build_arm(arms_col, (mats["metal"], mats["body"], mats["orange"]), name, shoulder, home_points[name])

    work_col = collection("Arms_Work_Inside_Outside", pose_col)
    build_arm(work_col, (mats["metal"], mats["body"], mats["orange"]), "A1_work_outside", home_shoulders["A1_LF"], [(2.0, -0.95, 2.75), (1.45, -1.75, 2.25), (0.75, -1.95, 1.75)])
    build_arm(work_col, (mats["metal"], mats["body"], mats["orange"]), "A2_work_inside", home_shoulders["A2_LR"], [(5.2, 0.65, 3.25), (4.55, 1.75, 2.55), (4.05, 2.45, 1.65)])
    build_arm(work_col, (mats["metal"], mats["body"], mats["orange"]), "A3_work_outside", home_shoulders["A3_RF"], [(2.0, 6.95, 2.75), (1.45, 7.75, 2.25), (0.75, 7.95, 1.75)])
    build_arm(work_col, (mats["metal"], mats["body"], mats["orange"]), "A4_work_inside", home_shoulders["A4_RR"], [(5.2, 5.35, 3.25), (4.55, 4.25, 2.55), (4.05, 3.55, 1.65)])
    work_col.hide_viewport = True
    work_col.hide_render = True

    dock_col = collection("Arms_Cooperative_Dock", pose_col)
    build_arm(dock_col, (mats["metal"], mats["body"], mats["orange"]), "A2_dock_left", home_shoulders["A2_LR"], [(5.1, 0.55, 3.15), (4.35, 1.55, 3.05), (4.0, 2.65, 2.95)])
    build_arm(dock_col, (mats["metal"], mats["body"], mats["orange"]), "A4_dock_right", home_shoulders["A4_RR"], [(5.1, 5.45, 3.15), (4.35, 4.45, 3.05), (4.0, 3.35, 2.95)])
    cyl_between("docking_alignment_bar_tip_to_tip", (4.0, 2.65, 2.95), (4.0, 3.35, 2.95), 0.035, mats["orange"], dock_col)
    dock_col.hide_viewport = True
    dock_col.hide_render = True

    # Mobility reference: eight wheel modules.
    for side_y, side in [(0.18, "left"), (5.82, "right")]:
        for idx, x in enumerate([0.9, 1.65, 6.35, 7.1], 1):
            bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=0.36, depth=0.26, location=(x, side_y, 0.30), rotation=(math.radians(90), 0, 0))
            wheel = bpy.context.object
            wheel.name = f"{side}_reference_wheel_module_{idx}"
            wheel.data.materials.append(mats["dark"])
            link_to_collection(wheel, mobility_col)
            cube_obj(f"{side}_wheel_suspension_block_{idx}", (x, side_y, 0.72), (0.48, 0.22, 0.42), mats["metal"], mobility_col)

    # Sensors from manifest, converted mm to meters.
    fixed_sensors = [
        ("S01", "wide camera", (0.3, 0.3, 3.85)), ("S02", "wide camera", (0.3, 5.7, 3.85)),
        ("S03", "wide camera", (7.7, 0.3, 3.85)), ("S04", "wide camera", (7.7, 5.7, 3.85)),
        ("S05", "hazard camera", (0.2, 0.35, 0.65)), ("S06", "hazard camera", (0.2, 5.65, 0.65)),
        ("S07", "hazard camera", (7.8, 0.35, 0.65)), ("S08", "hazard camera", (7.8, 5.65, 0.65)),
        ("S09", "LiDAR", (0.1, 3.0, 3.60)), ("S10", "LiDAR", (7.9, 3.0, 3.60)),
        ("S11", "radar depth", (4.0, 0.1, 2.50)), ("S12", "radar depth", (4.0, 5.9, 2.50)),
        ("S13", "bucket camera", (-0.5, 2.2, 1.50)), ("S14", "bucket camera", (-0.5, 3.8, 1.50)),
        ("S15", "bucket Y encoder", (0.0, 3.0, 3.35)), ("S16", "bucket Z encoder", (-0.15, 3.0, 0.95)),
        ("S17", "bucket load pin", (-0.65, 2.2, 1.0)), ("S18", "bucket load pin", (-0.65, 3.8, 1.0)),
        ("S19", "bucket tilt encoder", (-0.65, 3.0, 1.0)), ("S20", "feed fill flow", (0.35, 3.0, 3.45)),
        ("S21", "arm wrist camera", (2.8, -1.85, 4.15)), ("S22", "arm force torque", (2.8, -1.85, 3.95)),
        ("S23", "arm rail encoder", (2.2, -0.25, 3.15)), ("S24", "arm wrist camera", (4.7, 1.65, 3.95)),
        ("S25", "arm force torque", (4.7, 1.65, 3.75)), ("S26", "arm rail encoder", (5.8, -0.25, 3.15)),
        ("S27", "arm wrist camera", (2.8, 7.85, 4.15)), ("S28", "arm force torque", (2.8, 7.85, 3.95)),
        ("S29", "arm rail encoder", (2.2, 6.25, 3.15)), ("S30", "arm wrist camera", (4.7, 4.35, 3.95)),
        ("S31", "arm force torque", (4.7, 4.35, 3.75)), ("S32", "arm rail encoder", (5.8, 6.25, 3.15)),
        ("S33", "fill depth", (0.9, 0.9, 3.825)), ("S34", "fill depth", (0.9, 5.1, 3.825)),
        ("S35", "fill depth", (7.1, 0.9, 3.825)), ("S36", "fill depth", (7.1, 5.1, 3.825)),
        ("S37", "bin camera", (4.0, 3.0, 3.825)), ("S38", "dust visibility", (4.0, 3.0, 3.4)),
        ("S39", "drive load speed", (1.0, 0.3, 0.45)), ("S40", "drive load speed", (1.0, 5.7, 0.45)),
        ("S41", "drive load speed", (7.0, 0.3, 0.45)), ("S42", "drive load speed", (7.0, 5.7, 0.45)),
        ("S43", "IMU", (4.0, 3.0, 1.2)), ("S44", "strain vibration", (4.0, 3.0, 0.45)),
        ("S45", "thermal camera", (4.2, 0.0, 3.25)), ("S46", "thermal camera", (4.2, 6.0, 3.25)),
        ("S47", "dust accumulation", (4.0, 5.8, 3.9)), ("S48", "power health", (7.2, 3.0, 0.65)),
    ]
    for sid, stype, loc in fixed_sensors:
        sensor_marker(sid, stype, loc, sensors_col, mats)

    # Lunar context.
    cube_obj("lunar_regolith_ground_plane", (4.0, 3.0, -0.035), (13.0, 11.0, 0.06), mats["regolith"], lunar_col)
    for i in range(45):
        x = random.uniform(-2.0, 10.0)
        y = random.uniform(-2.5, 8.5)
        if 0.0 < x < 8.0 and 0.0 < y < 6.0:
            continue
        rock = sphere_obj(f"lunar_rock_{i+1:02d}", (x, y, random.uniform(0.02, 0.08)), random.uniform(0.05, 0.18), mats["regolith"], lunar_col, segments=8)
        rock.scale.z = random.uniform(0.25, 0.65)

    # Labels, datum, and scale.
    add_label("label_open_bin", "OPEN REGOLITH BIN - NO ROOF", (3.8, 3.0, 4.55), 0.22, root_col, mats["label"])
    add_label("label_front_bucket", "FRONT SLIDING-LIFT TOOTHED BUCKET", (-1.35, 3.0, 1.55), 0.16, root_col, mats["label"])
    add_label("label_four_arms", "4 RAIL-MOUNTED LONG-REACH ARMS", (4.0, 6.9, 3.65), 0.16, root_col, mats["label"])
    add_label("label_rear_service", "REAR SERVICE HATCH / UNDERFLOOR DECK", (8.55, 3.0, 1.2), 0.15, root_col, mats["label"])
    add_label("label_reference_mobility", "PROVISIONAL WHEELED MOBILITY - REFERENCE ONLY", (4.0, -0.85, 0.55), 0.13, root_col, mats["label"])
    cyl_between("datum_X_axis_front_to_rear", (0, 0, 0.05), (1.0, 0, 0.05), 0.018, mats["orange"], root_col)
    cyl_between("datum_Y_axis_left_to_right", (0, 0, 0.08), (0, 1.0, 0.08), 0.018, mats["lidar"], root_col)
    cyl_between("datum_Z_axis_vertical", (0, 0, 0.0), (0, 0, 1.0), 0.018, mats["camera"], root_col)
    add_label("label_datum", "DATUM X0 Y0 Z0", (-0.35, -0.2, 0.4), 0.10, root_col, mats["label"])
    cube_obj("scale_bar_2m", (1.0, -1.15, 0.05), (2.0, 0.06, 0.06), mats["orange"], root_col)
    add_label("label_scale_bar", "2 m", (1.0, -1.35, 0.20), 0.11, root_col, mats["label"])

    # Store engineering metadata.
    scene["CONTAINER_v2_body_envelope_m"] = "8.0 x 6.0 x 4.0"
    scene["CONTAINER_v2_raised_floor_z_m"] = 0.9
    scene["CONTAINER_v2_arm_rail_z_m"] = 3.15
    scene["CONTAINER_v2_bucket_width_m"] = 2.0
    scene["CONTAINER_v2_exclusions"] = "no gantry, anchors, stabilizers, outriggers, leveling legs, closed roof, or lid"
    scene["CONTAINER_v2_pose_states"] = "Bucket_Home_Low_Scoop; Bucket_Raised_Dump; Arms_Home; Arms_Work_Inside_Outside; Arms_Cooperative_Dock"

    # Lighting and world.
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 8))
    sun = bpy.context.object
    sun.name = "low_angle_lunar_sun"
    sun.rotation_euler = (math.radians(42), 0, math.radians(-38))
    sun.data.energy = 3.0
    bpy.ops.object.light_add(type="AREA", location=(2.0, -3.5, 6.0))
    area = bpy.context.object
    area.name = "soft_engineering_fill_light"
    area.data.energy = 360
    area.data.size = 5.0
    scene.world.color = (0.015, 0.016, 0.018)

    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))

    # Cameras and fast engineering preview renders. The .blend is saved first so
    # the model survives even if a local renderer stalls or crashes.
    render_camera("front_left_perspective", (-4.2, -5.2, 4.2), (4.0, 3.0, 2.1), 26)
    render_camera("top_orthographic", (4.0, 3.0, 13.0), (4.0, 3.0, 0.0), 35, ortho=True, ortho_scale=11.0)
    render_camera("right_side_elevation", (4.0, 13.0, 2.4), (4.0, 3.0, 2.2), 45, ortho=True, ortho_scale=8.8)
    render_camera("rear_service_view", (12.4, 3.0, 2.1), (7.6, 3.0, 1.8), 45, ortho=True, ortho_scale=7.2)
    render_camera("bucket_arm_detail_view", (-3.3, -3.8, 2.7), (1.8, 2.4, 2.1), 36)

    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    print(f"SAVED_BLEND={BLEND_PATH}")
    print(f"RENDER_DIR={RENDER_DIR}")
    print(f"OBJECT_COUNT={len(bpy.data.objects)}")
    print(f"COLLECTION_COUNT={len(bpy.data.collections)}")


if __name__ == "__main__":
    import traceback

    try:
        main()
        LOG_PATH.write_text("CONTAINER v2 Blender build completed successfully.\n", encoding="utf-8")
    except Exception:
        LOG_PATH.write_text(traceback.format_exc(), encoding="utf-8")
        raise
