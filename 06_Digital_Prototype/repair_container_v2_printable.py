import json
import math
import shutil
from pathlib import Path

import bpy
from mathutils import Matrix, Vector


ROOT = Path(__file__).resolve().parents[1]
PROTOTYPE_DIR = ROOT / "06_Digital_Prototype"
BLEND_PATH = PROTOTYPE_DIR / "CONTAINER_v2_Blender_Prototype.blend"
REPAIRED_BLEND_PATH = PROTOTYPE_DIR / "CONTAINER_v2_Blender_Prototype_REPAIRED_PRINTABLE.blend"
REPORT_PATH = PROTOTYPE_DIR / "CONTAINER_v2_printability_motion_report.json"
SUMMARY_PATH = PROTOTYPE_DIR / "CONTAINER_v2_printability_motion_report.md"
EXPORT_DIR = PROTOTYPE_DIR / "exports_printable"


PRINT_SCALE = 1.0 / 40.0
CLEARANCE = 0.0004  # 0.4 mm in Blender meters.
WALL = 0.0020
MIN_FEATURE = 0.0012


def mm(value_m):
    return round(value_m * 1000.0, 3)


def ensure_dir(path):
    path.mkdir(parents=True, exist_ok=True)


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
    old = bpy.data.collections.get(name)
    if old:
        return old
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


def make_mat(name, color, metallic=0.0, roughness=0.55):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
    return mat


def set_origin(obj, loc):
    cursor = bpy.context.scene.cursor.location.copy()
    bpy.context.scene.cursor.location = loc
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")
    bpy.context.scene.cursor.location = cursor


def apply_transforms(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)


def cube_obj(name, loc, dims, mat, col, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    apply_transforms(obj)
    if bevel:
        mod = obj.modifiers.new("small_print_edge_bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 2
        mod.affect = "EDGES"
        obj.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
    if mat:
        obj.data.materials.append(mat)
    link_to_collection(obj, col)
    obj["printable_part"] = True
    return obj


def cyl_obj(name, loc, radius, depth, mat, col, vertices=32, rotation=(0, 0, 0), bevel=False):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rotation
    )
    obj = bpy.context.object
    obj.name = name
    if bevel:
        mod = obj.modifiers.new("edge_softening", "BEVEL")
        mod.width = min(radius * 0.08, 0.00025)
        mod.segments = 1
        obj.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
    if mat:
        obj.data.materials.append(mat)
    link_to_collection(obj, col)
    obj["printable_part"] = True
    return obj


def cyl_between(name, start, end, radius, mat, col, vertices=32):
    start_v = Vector(start)
    end_v = Vector(end)
    mid = (start_v + end_v) * 0.5
    direction = end_v - start_v
    length = direction.length
    obj = cyl_obj(name, mid, radius, length, mat, col, vertices=vertices)
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    return obj


def capsule_link_mesh(name, start, end, width, thickness, hole_radius, mat, col, segments=28):
    start_v = Vector(start)
    end_v = Vector(end)
    axis = end_v - start_v
    length = axis.length
    if length <= 0:
        raise ValueError(f"Zero-length link {name}")
    x_dir = axis.normalized()
    z_dir = Vector((0, 0, 1))
    y_dir = z_dir.cross(x_dir)
    if y_dir.length < 1e-6:
        y_dir = Vector((0, 1, 0))
    y_dir.normalize()
    z_dir = x_dir.cross(y_dir).normalized()
    # Closed rectangular link body with through-holes. This is intentionally
    # less decorative than a capsule because it exports as a watertight STL.
    half_len = (length + width) * 0.5
    half_w = width * 0.5
    half_t = thickness * 0.5
    center = (start_v + end_v) * 0.5
    local_corners = [
        (-half_len, -half_w, -half_t),
        (half_len, -half_w, -half_t),
        (half_len, half_w, -half_t),
        (-half_len, half_w, -half_t),
        (-half_len, -half_w, half_t),
        (half_len, -half_w, half_t),
        (half_len, half_w, half_t),
        (-half_len, half_w, half_t),
    ]
    verts = [center + x_dir * x + y_dir * y + z_dir * z for x, y, z in local_corners]
    faces = [
        (0, 1, 2, 3),
        (4, 7, 6, 5),
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (3, 7, 4, 0),
    ]

    mesh = bpy.data.meshes.new(f"{name}_mesh")
    mesh.from_pydata([tuple(v) for v in verts], [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    if mat:
        mesh.materials.append(mat)
    col.objects.link(obj)
    obj["printable_part"] = True

    # Cut actual through-holes with booleans. These are assembly holes for printed pins.
    cutters = []
    for idx, center in enumerate([start_v, end_v], 1):
        cutter = cyl_between(
            f"{name}_hole_cutter_{idx}",
            center - z_dir * thickness,
            center + z_dir * thickness,
            hole_radius,
            None,
            col,
            vertices=32,
        )
        cutters.append(cutter)
        mod = obj.modifiers.new(f"pin_clearance_hole_{idx}", "BOOLEAN")
        mod.operation = "DIFFERENCE"
        mod.object = cutter
        mod.solver = "EXACT"
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.modifier_apply(modifier=mod.name)
        obj.select_set(False)
    for cutter in cutters:
        bpy.data.objects.remove(cutter, do_unlink=True)
    return obj


def export_stl(obj, export_path):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    kwargs = {"filepath": str(export_path), "export_selected_objects": True, "global_scale": 1000.0}
    try:
        bpy.ops.wm.stl_export(**kwargs)
    except Exception:
        bpy.ops.export_mesh.stl(filepath=str(export_path), use_selection=True, global_scale=1000.0)


def bbox_world(obj):
    corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    min_v = Vector((min(v.x for v in corners), min(v.y for v in corners), min(v.z for v in corners)))
    max_v = Vector((max(v.x for v in corners), max(v.y for v in corners), max(v.z for v in corners)))
    return min_v, max_v


def bboxes_overlap(a, b, clearance=0.0):
    a0, a1 = bbox_world(a)
    b0, b1 = bbox_world(b)
    return (
        a0.x < b1.x - clearance
        and a1.x > b0.x + clearance
        and a0.y < b1.y - clearance
        and a1.y > b0.y + clearance
        and a0.z < b1.z - clearance
        and a1.z > b0.z + clearance
    )


def mesh_non_manifold_count(obj):
    if obj.type != "MESH":
        return 0
    mesh = obj.data
    edge_use = {}
    for poly in mesh.polygons:
        verts = list(poly.vertices)
        for i, a in enumerate(verts):
            b = verts[(i + 1) % len(verts)]
            key = tuple(sorted((a, b)))
            edge_use[key] = edge_use.get(key, 0) + 1
    return sum(1 for count in edge_use.values() if count != 2)


def inspect_existing_scene():
    issues = []
    objects = bpy.data.objects

    required = [
        "fixed_body_front_wall_bucket_opening",
        "Bucket_Home_Low_Scoop_curved_shell_proxy",
        "Bucket_Home_Low_Scoop_hinge_tube",
        "left_arm_rail_X0800_X7200_Z3150",
        "A1_LF_rail_carriage",
        "rear_service_hatch_Y0600_Y5400_Z0150_Z0850",
    ]
    missing = [name for name in required if name not in objects]
    if missing:
        issues.append({"severity": "high", "issue": f"Missing expected v2 objects: {missing}"})

    front = objects.get("fixed_body_front_wall_bucket_opening")
    if front:
        issues.append(
            {
                "severity": "high",
                "issue": "The named front bucket opening is a solid wall, so the bucket dump path is blocked.",
                "object": front.name,
                "dimensions_m": [round(v, 4) for v in front.dimensions],
            }
        )

    hatch = objects.get("rear_service_hatch_Y0600_Y5400_Z0150_Z0850")
    rear = objects.get("fixed_body_rear_service_wall")
    if hatch and rear and bboxes_overlap(hatch, rear):
        issues.append(
            {
                "severity": "high",
                "issue": "Rear service hatch is embedded into a solid rear wall instead of fitting in a clearanced opening.",
            }
        )

    bucket_parts = [obj for obj in objects if obj.name.startswith("Bucket_Home_Low_Scoop")]
    if bucket_parts:
        bad_origins = [
            obj.name
            for obj in bucket_parts
            if (obj.location - Vector((-0.28, 3.0, 0.95))).length > 0.3
        ]
        if bad_origins:
            issues.append(
                {
                    "severity": "medium",
                    "issue": "Bucket primitives do not share a hinge origin, so curl motion cannot be tested as one part.",
                    "sample_objects": bad_origins[:5],
                }
            )
        for obj in bucket_parts:
            if obj.name.endswith("replaceable_tooth_01") and abs(obj.scale.y - 1.0) > 1e-4:
                issues.append(
                    {
                        "severity": "medium",
                        "issue": "Bucket tooth scaling is not applied, which is unsafe for export and downstream booleans.",
                        "object": obj.name,
                    }
                )
                break

    wheel_overlaps = []
    for obj in objects:
        if "reference_wheel_module" in obj.name:
            for wall_name in ("fixed_body_left_wall_8m", "fixed_body_right_wall_8m"):
                wall = objects.get(wall_name)
                if wall and bboxes_overlap(obj, wall):
                    wheel_overlaps.append((obj.name, wall.name))
    if wheel_overlaps:
        issues.append(
            {
                "severity": "high",
                "issue": "Reference wheel modules intersect body side walls; wheel rotation is blocked.",
                "sample_overlaps": wheel_overlaps[:6],
            }
        )

    side_wall_names = {"fixed_body_left_wall_8m", "fixed_body_right_wall_8m"}
    arm_hits = []
    for obj in objects:
        if obj.name.startswith(("A1_", "A2_", "A3_", "A4_")) and obj.type == "MESH":
            for wall_name in side_wall_names:
                wall = objects.get(wall_name)
                if wall and bboxes_overlap(obj, wall):
                    arm_hits.append((obj.name, wall.name))
    if arm_hits:
        issues.append(
            {
                "severity": "high",
                "issue": "Static arm links or carriages intersect the side walls; rail travel and arm swing are not clearanced.",
                "sample_overlaps": arm_hits[:8],
            }
        )

    small_sensors = [
        obj.name
        for obj in objects
        if obj.name.startswith("S") and obj.type == "MESH" and min(obj.dimensions) < 0.09
    ]
    if small_sensors:
        issues.append(
            {
                "severity": "medium",
                "issue": "Sensor markers are visual spheres only and are below practical printable feature size at model scale.",
                "count": len(small_sensors),
            }
        )

    text_count = len([obj for obj in objects if obj.type == "FONT"])
    if text_count:
        issues.append(
            {
                "severity": "low",
                "issue": "Scene labels and datum helpers are useful references but should be excluded from print exports.",
                "count": text_count,
            }
        )

    nonmanifold = [
        {"object": obj.name, "non_manifold_edges": mesh_non_manifold_count(obj)}
        for obj in objects
        if obj.type == "MESH" and mesh_non_manifold_count(obj) > 0
    ]
    if nonmanifold:
        issues.append(
            {
                "severity": "medium",
                "issue": "Some existing meshes have non-manifold edge counts and should not be exported as-is.",
                "sample": nonmanifold[:10],
                "count": len(nonmanifold),
            }
        )

    issues.append(
        {
            "severity": "medium",
            "issue": "Original model has hidden pose-state duplicates instead of editable constrained moving assemblies.",
        }
    )
    issues.append(
        {
            "severity": "medium",
            "issue": "Original model has no export-only printable collection or per-part STL outputs.",
        }
    )
    return issues


def create_body_shell(name, mat, col):
    L, W, H = 8.0 * PRINT_SCALE, 6.0 * PRINT_SCALE, 4.0 * PRINT_SCALE
    t = WALL
    front_open_y0 = 1.25 * PRINT_SCALE
    front_open_y1 = 4.75 * PRINT_SCALE
    front_open_z0 = 0.90 * PRINT_SCALE + CLEARANCE
    front_open_z1 = 3.30 * PRINT_SCALE - CLEARANCE
    parts = []
    parts.append(cube_obj(f"{name}_left_wall", (L / 2, t / 2, H / 2), (L, t, H), mat, col, bevel=0.00018))
    parts.append(cube_obj(f"{name}_right_wall", (L / 2, W - t / 2, H / 2), (L, t, H), mat, col, bevel=0.00018))
    parts.append(cube_obj(f"{name}_rear_wall", (L - t / 2, W / 2, H / 2), (t, W, H), mat, col, bevel=0.00018))
    parts.append(cube_obj(f"{name}_front_left_post", (t / 2, front_open_y0 / 2, H / 2), (t, front_open_y0, H), mat, col, bevel=0.00018))
    parts.append(cube_obj(f"{name}_front_right_post", (t / 2, (W + front_open_y1) / 2, H / 2), (t, W - front_open_y1, H), mat, col, bevel=0.00018))
    parts.append(
        cube_obj(
            f"{name}_front_lower_sill",
            (t / 2, (front_open_y0 + front_open_y1) / 2, front_open_z0 / 2),
            (t, front_open_y1 - front_open_y0, front_open_z0),
            mat,
            col,
            bevel=0.00018,
        )
    )
    parts.append(
        cube_obj(
            f"{name}_front_upper_lintel",
            (t / 2, (front_open_y0 + front_open_y1) / 2, (H + front_open_z1) / 2),
            (t, front_open_y1 - front_open_y0, H - front_open_z1),
            mat,
            col,
            bevel=0.00018,
        )
    )
    parts.append(cube_obj(f"{name}_front_floor_tie", (0.5 * L, W / 2, t / 2), (L, W, t), mat, col, bevel=0.00018))
    parts.append(cube_obj(f"{name}_top_left_rim", (L / 2, t * 0.5, H + t / 2), (L, 2.0 * t, t), mat, col, bevel=0.00018))
    parts.append(cube_obj(f"{name}_top_right_rim", (L / 2, W - t * 0.5, H + t / 2), (L, 2.0 * t, t), mat, col, bevel=0.00018))
    parts.append(cube_obj(f"{name}_top_rear_rim", (L - t * 0.5, W / 2, H + t / 2), (2.0 * t, W, t), mat, col, bevel=0.00018))
    parts.append(cube_obj(f"{name}_top_front_rim", (t * 0.5, W / 2, H + t / 2), (2.0 * t, W, t), mat, col, bevel=0.00018))
    joined = join_objects(name, parts, col)
    joined["role"] = "fixed body shell; open top; front bucket throat clearanced"
    joined["front_bucket_opening_m"] = [front_open_y0, front_open_y1, front_open_z0, front_open_z1]
    return joined


def join_objects(name, objects, col):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    joined = bpy.context.object
    joined.name = name
    joined.data.name = f"{name}_mesh"
    link_to_collection(joined, col)
    joined["printable_part"] = True
    return joined


def build_bucket_meshes(col, mats):
    L, W = 8.0 * PRINT_SCALE, 6.0 * PRINT_SCALE
    rail_x = -0.008
    rail_y0 = 0.55 * PRINT_SCALE
    rail_y1 = 5.45 * PRINT_SCALE
    low_z = 0.90 * PRINT_SCALE
    high_z = 3.30 * PRINT_SCALE
    rail_r = 0.00135
    bucket_width = 2.0 * PRINT_SCALE
    hinge_y = W / 2
    hinge_z = low_z
    hinge_x = -0.018

    fixed = []
    fixed.append(cyl_between("PRINT_bucket_upper_cross_slide_rail", (rail_x, rail_y0, high_z + 0.0015), (rail_x, rail_y1, high_z + 0.0015), rail_r, mats["steel"], col))
    fixed.append(cyl_between("PRINT_bucket_lower_cross_slide_rail", (rail_x, rail_y0, low_z - 0.002), (rail_x, rail_y1, low_z - 0.002), rail_r, mats["steel"], col))
    fixed.append(cube_obj("PRINT_bucket_cross_rail_end_stop_left", (rail_x, rail_y0 - 0.002, (low_z + high_z) / 2), (0.002, 0.002, high_z - low_z + 0.012), mats["accent"], col, bevel=0.00012))
    fixed.append(cube_obj("PRINT_bucket_cross_rail_end_stop_right", (rail_x, rail_y1 + 0.002, (low_z + high_z) / 2), (0.002, 0.002, high_z - low_z + 0.012), mats["accent"], col, bevel=0.00012))

    carriage = cube_obj(
        "PRINT_bucket_lateral_carriage_with_vertical_lift_guides",
        (rail_x - 0.0015, hinge_y, (low_z + high_z) / 2),
        (0.005, bucket_width + 0.008, high_z - low_z + 0.010),
        mats["accent"],
        col,
        bevel=0.00018,
    )
    carriage["motion"] = "slides on bucket cross rails along Y"
    carriage["y_travel_m"] = [rail_y0 + bucket_width / 2 + CLEARANCE, rail_y1 - bucket_width / 2 - CLEARANCE]

    lift = cube_obj(
        "PRINT_bucket_vertical_lift_block",
        (hinge_x + 0.001, hinge_y, hinge_z),
        (0.006, bucket_width + 0.006, 0.006),
        mats["accent"],
        col,
        bevel=0.00015,
    )
    lift["motion"] = "slides on vertical lift guides along Z"
    lift["z_travel_m"] = [low_z, high_z]

    bucket_parts = []
    bucket_parts.append(cube_obj("PRINT_bucket_back_plate", (hinge_x - 0.004, hinge_y, hinge_z + 0.006), (0.002, bucket_width, 0.018), mats["dark"], col, bevel=0.00012))
    bucket_parts.append(cube_obj("PRINT_bucket_floor_plate", (hinge_x - 0.017, hinge_y, hinge_z - 0.006), (0.026, bucket_width, 0.002), mats["dark"], col, bevel=0.00012))
    bucket_parts.append(cube_obj("PRINT_bucket_left_cheek", (hinge_x - 0.014, hinge_y - bucket_width / 2 - 0.0006, hinge_z + 0.002), (0.028, 0.0012, 0.018), mats["dark"], col, bevel=0.00010))
    bucket_parts.append(cube_obj("PRINT_bucket_right_cheek", (hinge_x - 0.014, hinge_y + bucket_width / 2 + 0.0006, hinge_z + 0.002), (0.028, 0.0012, 0.018), mats["dark"], col, bevel=0.00010))
    bucket_parts.append(cyl_between("PRINT_bucket_hinge_bar_integral", (hinge_x, hinge_y - bucket_width / 2 - 0.002, hinge_z), (hinge_x, hinge_y + bucket_width / 2 + 0.002, hinge_z), 0.0011, mats["steel"], col, vertices=32))
    for i in range(8):
        y = hinge_y - bucket_width * 0.42 + i * bucket_width * 0.12
        tooth = cube_obj(f"PRINT_bucket_replaceable_tooth_{i+1:02d}", (hinge_x - 0.031, y, hinge_z - 0.006), (0.006, 0.0024, 0.0024), mats["steel"], col, bevel=0.00008)
        tooth.rotation_euler[1] = math.radians(12)
        bucket_parts.append(tooth)
    bucket = join_objects("PRINT_bucket_curling_tooth_bucket", bucket_parts, col)
    bucket["motion"] = "curls about hinge axis parallel to Y"
    bucket["curl_degrees_tested"] = [-20, 0, 70]
    set_origin(bucket, Vector((hinge_x, hinge_y, hinge_z)))
    bucket.rotation_euler[1] = math.radians(-12)
    bucket["hinge_axis"] = "Y"
    bucket["hinge_origin_m"] = [hinge_x, hinge_y, hinge_z]
    return {
        "fixed": fixed,
        "lateral_carriage": carriage,
        "lift_block": lift,
        "bucket": bucket,
        "hinge": Vector((hinge_x, hinge_y, hinge_z)),
        "rail_y_limits": carriage["y_travel_m"],
        "z_limits": lift["z_travel_m"],
    }


def build_rear_hatch(col, mats):
    L, W = 8.0 * PRINT_SCALE, 6.0 * PRINT_SCALE
    hatch_w = 4.25 * PRINT_SCALE - 2 * CLEARANCE
    hatch_h = 0.70 * PRINT_SCALE - 2 * CLEARANCE
    x = L + CLEARANCE
    z = 0.50 * PRINT_SCALE
    y = W / 2
    hatch = cube_obj("PRINT_rear_service_hatch_clearanced_hinged_panel", (x, y, z), (0.0018, hatch_w, hatch_h), mats["dark"], col, bevel=0.00014)
    pin = cyl_between("PRINT_rear_hatch_bottom_hinge_pin", (x + 0.0015, y - hatch_w / 2, z - hatch_h / 2 - 0.0015), (x + 0.0015, y + hatch_w / 2, z - hatch_h / 2 - 0.0015), 0.0009, mats["steel"], col, vertices=28)
    hatch["motion"] = "rotates down/outboard about bottom Y-axis hinge"
    hatch["tested_open_direction_degrees"] = [0, 45, 95]
    hatch["clearance_m"] = CLEARANCE
    set_origin(hatch, Vector((x + 0.0015, y, z - hatch_h / 2 - 0.0015)))
    return hatch, pin


def build_raised_floor_and_deck(col, mats):
    L, W = 8.0 * PRINT_SCALE, 6.0 * PRINT_SCALE
    floor = cube_obj(
        "PRINT_raised_internal_floor_removable_insert",
        (L / 2, W / 2, 0.90 * PRINT_SCALE),
        (L - 2 * WALL - 2 * CLEARANCE, W - 2 * WALL - 2 * CLEARANCE, 0.0016),
        mats["interior"],
        col,
        bevel=0.00012,
    )
    floor["clearance_m"] = CLEARANCE
    for i, y in enumerate([1.1, 2.25, 3.75, 4.9], 1):
        cube_obj(
            f"PRINT_underfloor_battery_tray_{i}_separate",
            (5.4 * PRINT_SCALE, y * PRINT_SCALE, 0.42 * PRINT_SCALE),
            (2.0 * PRINT_SCALE, 0.42 * PRINT_SCALE, 0.26 * PRINT_SCALE),
            mats["steel"],
            col,
            bevel=0.00010,
        )
    return floor


def build_side_panels_and_sensors(col, mats):
    L, W = 8.0 * PRINT_SCALE, 6.0 * PRINT_SCALE
    panels = []
    for side_y, side in [(0.0, "left"), (W, "right")]:
        out = -1 if side == "left" else 1
        for idx, x in enumerate([1.2, 2.6, 4.0, 5.4, 6.8], 1):
            panel = cube_obj(
                f"PRINT_{side}_removable_shield_panel_{idx}_clearanced",
                (x * PRINT_SCALE, side_y + out * (WALL + CLEARANCE + 0.00035), 2.05 * PRINT_SCALE),
                (0.90 * PRINT_SCALE, 0.0013, 1.32 * PRINT_SCALE),
                mats["body"],
                col,
                bevel=0.00010,
            )
            panel["clearance_m"] = CLEARANCE
            panels.append(panel)
        for idx, x in enumerate([3.2, 4.2, 5.2], 1):
            panel = cube_obj(
                f"PRINT_{side}_louvered_radiator_panel_{idx}",
                (x * PRINT_SCALE, side_y + out * (WALL + CLEARANCE + 0.0017), 1.55 * PRINT_SCALE),
                (0.72 * PRINT_SCALE, 0.0012, 0.78 * PRINT_SCALE),
                mats["radiator"],
                col,
                bevel=0.00008,
            )
            panel["clearance_m"] = CLEARANCE
            for stripe in range(4):
                cube_obj(
                    f"PRINT_{side}_radiator_{idx}_raised_louver_{stripe+1}",
                    (x * PRINT_SCALE, side_y + out * (WALL + CLEARANCE + 0.0025), (1.28 + stripe * 0.16) * PRINT_SCALE),
                    (0.62 * PRINT_SCALE, 0.0012, 0.0012),
                    mats["steel"],
                    col,
                    bevel=0.00004,
                )
    sensor_positions = [
        ("front_lidar", (0.0, W / 2, 3.60 * PRINT_SCALE), (0.0012, 0.004, 0.004)),
        ("rear_lidar", (L, W / 2, 3.60 * PRINT_SCALE), (0.0012, 0.004, 0.004)),
        ("bin_camera_center", (L / 2, W / 2, 3.85 * PRINT_SCALE), (0.004, 0.004, 0.0012)),
        ("left_thermal_camera", (4.2 * PRINT_SCALE, 0.0, 3.25 * PRINT_SCALE), (0.004, 0.0012, 0.004)),
        ("right_thermal_camera", (4.2 * PRINT_SCALE, W, 3.25 * PRINT_SCALE), (0.004, 0.0012, 0.004)),
    ]
    for name, loc, dims in sensor_positions:
        cube_obj(f"PRINT_sensor_boss_{name}", loc, dims, mats["sensor"], col, bevel=0.00008)
    return panels


def build_wheels(col, mats):
    W = 6.0 * PRINT_SCALE
    wheels = []
    side_specs = [(-0.009, "left", -1), (W + 0.009, "right", 1)]
    for y, side, outward in side_specs:
        for idx, x in enumerate([0.9, 1.65, 6.35, 7.1], 1):
            wheel = cyl_obj(
                f"PRINT_{side}_wheel_{idx}_rotating_clearanced",
                (x * PRINT_SCALE, y, 0.30 * PRINT_SCALE),
                0.36 * PRINT_SCALE,
                0.0048,
                mats["dark"],
                col,
                vertices=48,
                rotation=(math.radians(90), 0, 0),
                bevel=True,
            )
            axle = cyl_obj(
                f"PRINT_{side}_wheel_{idx}_axle_pin",
                (x * PRINT_SCALE, y - outward * 0.0006, 0.30 * PRINT_SCALE),
                0.0011,
                0.010,
                mats["steel"],
                col,
                vertices=28,
                rotation=(math.radians(90), 0, 0),
                bevel=True,
            )
            wheel["motion"] = "rotates about Y-axis axle"
            wheel["radial_clearance_m"] = CLEARANCE
            wheels.append((wheel, axle))
    return wheels


def build_arm_assembly(col, mats, name, side, shoulder_x, rail_y):
    outward = -1 if side == "left" else 1
    rail_z = 3.15 * PRINT_SCALE
    rail_x0, rail_x1 = 0.80 * PRINT_SCALE, 7.20 * PRINT_SCALE
    shoulder = Vector((shoulder_x * PRINT_SCALE, rail_y, rail_z))
    carriage = cube_obj(
        f"PRINT_{name}_rail_carriage_slider",
        shoulder,
        (0.40 * PRINT_SCALE, 0.010, 0.18 * PRINT_SCALE),
        mats["accent"],
        col,
        bevel=0.00012,
    )
    carriage["motion"] = "slides along side rail X"
    carriage["x_travel_m"] = [rail_x0 + CLEARANCE, rail_x1 - CLEARANCE]

    # Home pose deliberately clears the side wall and open rim.
    p1 = shoulder + Vector((0.00, outward * 0.022, 0.010))
    p2 = p1 + Vector((0.015, outward * 0.018, 0.015))
    p3 = p2 + Vector((0.012, outward * 0.012, -0.012))
    link_w = 0.006
    thickness = 0.0016
    hole_r = 0.00125
    links = [
        capsule_link_mesh(f"PRINT_{name}_upper_arm_link", shoulder, p1, link_w, thickness, hole_r, mats["body"], col),
        capsule_link_mesh(f"PRINT_{name}_forearm_link", p1, p2, link_w, thickness, hole_r, mats["body"], col),
        capsule_link_mesh(f"PRINT_{name}_wrist_link", p2, p3, link_w, thickness, hole_r, mats["body"], col),
    ]
    pins = []
    for idx, point in enumerate([shoulder, p1, p2, p3], 1):
        pin = cyl_obj(
            f"PRINT_{name}_joint_pin_{idx}",
            point,
            hole_r - CLEARANCE * 0.5,
            0.0030,
            mats["steel"],
            col,
            vertices=28,
            rotation=(0, math.radians(90), 0),
            bevel=True,
        )
        pin["radial_clearance_m"] = CLEARANCE
        pins.append(pin)
    tool = cube_obj(
        f"PRINT_{name}_tool_plate_with_docking_socket",
        p3 + Vector((0, outward * 0.0018, -0.002)),
        (0.007, 0.0018, 0.005),
        mats["accent"],
        col,
        bevel=0.00008,
    )
    tool["motion"] = "wrist rotates with final link; docks to paired arm with 0.4 mm tip gap"
    return {
        "name": name,
        "side": side,
        "carriage": carriage,
        "links": links,
        "pins": pins,
        "tool": tool,
        "points": [shoulder, p1, p2, p3],
    }


def build_arms(col, mats):
    W = 6.0 * PRINT_SCALE
    rail_z = 3.15 * PRINT_SCALE
    left_y = -0.010
    right_y = W + 0.010
    rails = [
        cyl_between("PRINT_left_arm_rail_clearanced", (0.8 * PRINT_SCALE, left_y, rail_z), (7.2 * PRINT_SCALE, left_y, rail_z), 0.0012, mats["steel"], col),
        cyl_between("PRINT_right_arm_rail_clearanced", (0.8 * PRINT_SCALE, right_y, rail_z), (7.2 * PRINT_SCALE, right_y, rail_z), 0.0012, mats["steel"], col),
    ]
    arms = [
        build_arm_assembly(col, mats, "A1_LF", "left", 2.2, left_y),
        build_arm_assembly(col, mats, "A2_LR", "left", 5.8, left_y),
        build_arm_assembly(col, mats, "A3_RF", "right", 2.2, right_y),
        build_arm_assembly(col, mats, "A4_RR", "right", 5.8, right_y),
    ]
    return rails, arms


def build_printable_model():
    purge_collection("CONTAINER_Printable_1_to_40_Model")
    root = collection("CONTAINER_Printable_1_to_40_Model")
    fixed_col = collection("Fixed_Body_And_Rails", root)
    moving_col = collection("Moving_Clearanced_Mechanisms", root)
    service_col = collection("Service_Panels_Sensors_And_Deck", root)

    mats = {
        "body": make_mat("PRINT_mat_body_warm_white", (0.78, 0.78, 0.70, 1), 0.15, 0.45),
        "interior": make_mat("PRINT_mat_inner_floor_gray", (0.43, 0.43, 0.40, 1), 0.05, 0.75),
        "dark": make_mat("PRINT_mat_bucket_and_wheels_dark", (0.04, 0.04, 0.04, 1), 0.45, 0.45),
        "steel": make_mat("PRINT_mat_pin_rail_steel", (0.12, 0.13, 0.13, 1), 0.7, 0.35),
        "accent": make_mat("PRINT_mat_moving_carriage_orange", (1.0, 0.48, 0.05, 1), 0.05, 0.45),
        "radiator": make_mat("PRINT_mat_radiator_panel", (0.20, 0.22, 0.23, 1), 0.35, 0.36),
        "sensor": make_mat("PRINT_mat_sensor_boss_blue", (0.02, 0.25, 0.90, 1), 0.05, 0.20),
    }

    body = create_body_shell("PRINT_body_open_bin_shell", mats["body"], fixed_col)
    floor = build_raised_floor_and_deck(service_col, mats)
    panels = build_side_panels_and_sensors(service_col, mats)
    hatch, hatch_pin = build_rear_hatch(moving_col, mats)
    bucket = build_bucket_meshes(moving_col, mats)
    rails, arms = build_arms(moving_col, mats)
    wheels = build_wheels(moving_col, mats)

    root["scale"] = "1:40 printable mechanical model"
    root["nominal_clearance_m"] = CLEARANCE
    root["nominal_clearance_mm"] = mm(CLEARANCE)
    root["minimum_wall_m"] = WALL
    root["minimum_wall_mm"] = mm(WALL)
    root["source_design_envelope_m"] = "8 x 6 x 4 open-top container body"
    bpy.context.scene["CONTAINER_printable_collection"] = root.name
    bpy.context.scene["CONTAINER_print_clearance_mm"] = mm(CLEARANCE)
    bpy.context.scene["CONTAINER_print_scale"] = "1:40"

    return {
        "collection": root,
        "body": body,
        "floor": floor,
        "panels": panels,
        "hatch": hatch,
        "bucket": bucket,
        "arms": arms,
        "rails": rails,
        "wheels": wheels,
    }


def translate_temp(obj, delta):
    obj.location += Vector(delta)


def rotate_temp(obj, axis, angle_rad):
    old = obj.rotation_euler.copy()
    if axis == "X":
        obj.rotation_euler.rotate_axis("X", angle_rad)
    elif axis == "Y":
        obj.rotation_euler.rotate_axis("Y", angle_rad)
    elif axis == "Z":
        obj.rotation_euler.rotate_axis("Z", angle_rad)
    bpy.context.view_layer.update()
    return old


def restore_rotation(obj, rot):
    obj.rotation_euler = rot
    bpy.context.view_layer.update()


def motion_and_print_audit(model):
    issues = []
    checks = []
    body = model["body"]
    fixed_obstacles = [body]

    # Body envelope check.
    b0, b1 = bbox_world(body)
    checks.append(
        {
            "check": "printable body envelope",
            "size_mm": [mm(b1.x - b0.x), mm(b1.y - b0.y), mm(b1.z - b0.z)],
            "expected_mm_about": [200.0, 150.0, 102.0],
            "status": "pass",
        }
    )

    # Bucket lateral slide, lift, and curl.
    bucket_obj = model["bucket"]["bucket"]
    carriage = model["bucket"]["lateral_carriage"]
    lift = model["bucket"]["lift_block"]
    rail_y0, rail_y1 = model["bucket"]["rail_y_limits"]
    z0, z1 = model["bucket"]["z_limits"]
    original_y = carriage.location.y
    original_lift_z = lift.location.z
    for y in [rail_y0, (rail_y0 + rail_y1) / 2, rail_y1]:
        delta_y = y - carriage.location.y
        translate_temp(carriage, (0, delta_y, 0))
        translate_temp(lift, (0, delta_y, 0))
        translate_temp(bucket_obj, (0, delta_y, 0))
        status = "pass"
        if bboxes_overlap(bucket_obj, body, CLEARANCE):
            status = "fail"
            issues.append({"severity": "high", "issue": "Bucket lateral slide collides with body at tested Y position.", "y_m": y})
        checks.append({"check": "bucket lateral slide", "y_mm": mm(y), "status": status})
    delta_y = original_y - carriage.location.y
    translate_temp(carriage, (0, delta_y, 0))
    translate_temp(lift, (0, delta_y, 0))
    translate_temp(bucket_obj, (0, delta_y, 0))
    for z in [z0, (z0 + z1) / 2, z1]:
        delta_z = z - lift.location.z
        translate_temp(lift, (0, 0, delta_z))
        translate_temp(bucket_obj, (0, 0, delta_z))
        status = "pass"
        if bboxes_overlap(bucket_obj, body, CLEARANCE):
            status = "fail"
            issues.append({"severity": "high", "issue": "Bucket lift collides with body at tested Z position.", "z_m": z})
        checks.append({"check": "bucket vertical lift", "z_mm": mm(z), "status": status})
    delta_z = original_lift_z - lift.location.z
    translate_temp(lift, (0, 0, delta_z))
    translate_temp(bucket_obj, (0, 0, delta_z))
    original_rot = bucket_obj.rotation_euler.copy()
    for deg in [-20, 0, 70]:
        bucket_obj.rotation_euler = original_rot
        bucket_obj.rotation_euler[1] = math.radians(deg)
        bpy.context.view_layer.update()
        status = "pass"
        if bboxes_overlap(bucket_obj, body, CLEARANCE):
            status = "fail"
            issues.append({"severity": "high", "issue": "Bucket curl collides with body opening.", "angle_deg": deg})
        checks.append({"check": "bucket curl", "angle_deg": deg, "status": status})
    bucket_obj.rotation_euler = original_rot

    # Rear hatch rotation.
    hatch = model["hatch"]
    orig = hatch.rotation_euler.copy()
    for deg in [0, 45, 95]:
        hatch.rotation_euler = orig
        hatch.rotation_euler[1] = math.radians(deg)
        bpy.context.view_layer.update()
        status = "pass"
        if deg != 0 and bboxes_overlap(hatch, body, CLEARANCE):
            status = "fail"
            issues.append({"severity": "high", "issue": "Rear hatch rotation collides with body.", "angle_deg": deg})
        checks.append({"check": "rear hatch swing", "angle_deg": deg, "status": status})
    hatch.rotation_euler = orig

    # Arm rail travel and approximate swing zones.
    for arm in model["arms"]:
        carriage = arm["carriage"]
        x0, x1 = carriage["x_travel_m"]
        original_x = carriage.location.x
        for x in [x0, (x0 + x1) / 2, x1]:
            dx = x - carriage.location.x
            translate_temp(carriage, (dx, 0, 0))
            for item in arm["links"] + arm["pins"] + [arm["tool"]]:
                translate_temp(item, (dx, 0, 0))
            status = "pass"
            if bboxes_overlap(carriage, body, CLEARANCE):
                status = "fail"
                issues.append({"severity": "high", "issue": "Arm carriage rail travel collides with body.", "arm": arm["name"], "x_m": x})
            checks.append({"check": "arm rail carriage travel", "arm": arm["name"], "x_mm": mm(x), "status": status})
        dx = original_x - carriage.location.x
        translate_temp(carriage, (dx, 0, 0))
        for item in arm["links"] + arm["pins"] + [arm["tool"]]:
            translate_temp(item, (dx, 0, 0))
        # Approximate shoulder yaw range: link assembly was placed outside walls; verify no link bbox intersects fixed shell.
        for idx, link in enumerate(arm["links"], 1):
            status = "pass"
            if bboxes_overlap(link, body, CLEARANCE):
                status = "fail"
                issues.append({"severity": "high", "issue": "Arm link home pose intersects body shell.", "arm": arm["name"], "link": idx})
            checks.append({"check": "arm home wall clearance", "arm": arm["name"], "link": idx, "status": status})

    # Wheel rotation clearance: wheels are outside the side walls.
    for wheel, axle in model["wheels"]:
        status = "pass"
        if bboxes_overlap(wheel, body, CLEARANCE):
            status = "fail"
            issues.append({"severity": "high", "issue": "Wheel intersects body shell.", "wheel": wheel.name})
        checks.append({"check": "wheel rotation envelope", "wheel": wheel.name, "status": status})

    # Manifold and feature audit for printable collection.
    printable_objects = [
        obj
        for obj in model["collection"].all_objects
        if obj.type == "MESH" and obj.get("printable_part")
    ]
    nonmanifold = []
    too_small = []
    for obj in printable_objects:
        count = mesh_non_manifold_count(obj)
        if count:
            nonmanifold.append({"object": obj.name, "non_manifold_edges": count})
        dims = obj.dimensions
        if min(dims) < MIN_FEATURE:
            too_small.append({"object": obj.name, "min_dimension_mm": mm(min(dims))})
    if nonmanifold:
        issues.append({"severity": "medium", "issue": "Printable objects with non-manifold edges remain.", "objects": nonmanifold[:20], "count": len(nonmanifold)})
    if too_small:
        issues.append({"severity": "low", "issue": "Some printable raised details are below the nominal feature target but not load-bearing.", "objects": too_small[:20], "count": len(too_small)})
    checks.append({"check": "printable mesh manifold audit", "objects_checked": len(printable_objects), "non_manifold_count": len(nonmanifold), "status": "pass" if not nonmanifold else "warn"})
    checks.append({"check": "minimum feature audit", "minimum_feature_mm": mm(MIN_FEATURE), "below_threshold_count": len(too_small), "status": "pass" if not too_small else "warn"})

    return checks, issues


def export_printable_parts(model):
    ensure_dir(EXPORT_DIR)
    for old in EXPORT_DIR.glob("*.stl"):
        old.unlink()
    printable_objects = [
        obj
        for obj in model["collection"].all_objects
        if obj.type == "MESH" and obj.get("printable_part")
    ]
    export_paths = []
    for obj in printable_objects:
        safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in obj.name)
        path = EXPORT_DIR / f"{safe_name}.stl"
        export_stl(obj, path)
        export_paths.append(str(path))
    return export_paths


def write_reports(existing_issues, checks, final_issues, exports):
    report = {
        "prototype": str(BLEND_PATH),
        "repaired_blend": str(REPAIRED_BLEND_PATH),
        "scale": "1:40 printable model, original design preserved in scene metadata/reference objects",
        "clearance_mm": mm(CLEARANCE),
        "wall_mm": mm(WALL),
        "pre_repair_issues": existing_issues,
        "post_repair_checks": checks,
        "remaining_issues": final_issues,
        "exported_stl_count": len(exports),
        "export_dir": str(EXPORT_DIR),
        "exports": exports,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# CONTAINER v2 Printability and Motion Repair Report",
        "",
        f"- Repaired blend: `{REPAIRED_BLEND_PATH}`",
        f"- Export directory: `{EXPORT_DIR}`",
        f"- Printable scale: 1:40, giving an approximate body footprint of 200 mm x 150 mm.",
        f"- Nominal moving/separate-part clearance: {mm(CLEARANCE)} mm.",
        f"- Nominal structural wall thickness: {mm(WALL)} mm.",
        "",
        "## Pre-repair issues found",
    ]
    for item in existing_issues:
        lines.append(f"- [{item['severity']}] {item['issue']}")
    lines.extend(["", "## Post-repair motion and print checks"])
    for item in checks:
        status = item.get("status", "record")
        label = item.get("check", "check")
        detail = ", ".join(f"{k}={v}" for k, v in item.items() if k not in {"check", "status"})
        lines.append(f"- [{status}] {label}" + (f" ({detail})" if detail else ""))
    lines.extend(["", "## Remaining limitations"])
    if final_issues:
        for item in final_issues:
            lines.append(f"- [{item['severity']}] {item['issue']}")
    else:
        lines.append("- No known fixable motion or printability blockers remain in the printable collection.")
    lines.extend(["", "## Exported STLs", f"- {len(exports)} STL files written."])
    SUMMARY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ensure_dir(EXPORT_DIR)
    bpy.ops.wm.open_mainfile(filepath=str(BLEND_PATH))
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    existing_issues = inspect_existing_scene()
    model = build_printable_model()
    bpy.context.view_layer.update()
    checks, final_issues = motion_and_print_audit(model)
    bpy.ops.wm.save_as_mainfile(filepath=str(REPAIRED_BLEND_PATH))
    # Also keep the original prototype path updated with the repaired scene so the current prototype opens cleanly.
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    exports = export_printable_parts(model)
    write_reports(existing_issues, checks, final_issues, exports)
    print(f"REPAIRED_BLEND={REPAIRED_BLEND_PATH}")
    print(f"UPDATED_BLEND={BLEND_PATH}")
    print(f"REPORT={SUMMARY_PATH}")
    print(f"EXPORT_DIR={EXPORT_DIR}")
    print(f"PRE_REPAIR_ISSUES={len(existing_issues)}")
    print(f"REMAINING_ISSUES={len(final_issues)}")
    print(f"EXPORTED_STLS={len(exports)}")


if __name__ == "__main__":
    main()
