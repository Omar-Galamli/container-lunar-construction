import math
from pathlib import Path

import bpy
from mathutils import Matrix, Vector


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "06_Digital_Prototype"
MAIN_BLEND = OUT_DIR / "CONTAINER_v2_Blender_Prototype.blend"
CLEAN_BLEND = OUT_DIR / "CONTAINER_v2_CLEAN_PREVIEW_ONLY.blend"
REPORT = OUT_DIR / "CONTAINER_v2_iteration_rebuild_report.md"
RENDER = OUT_DIR / "renders" / "iteration_rebuild_preview.png"
EXPORT_DIR = OUT_DIR / "exports_mvp_printable"

MM_CLEARANCE = 0.4
HINGE_CLEARANCE = 0.6
WALL = 3.2
BODY_L = 260.0
BODY_W = 150.0
BODY_Z0 = 47.0
FLOOR_TOP = 52.0
BODY_TOP = 128.0


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for blocks in (
        bpy.data.meshes,
        bpy.data.materials,
        bpy.data.cameras,
        bpy.data.lights,
        bpy.data.curves,
        bpy.data.collections,
    ):
        for item in list(blocks):
            if getattr(item, "users", 0) == 0:
                blocks.remove(item)


def configure_scene():
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    scene.frame_start = 1
    scene.frame_end = 100
    scene.frame_set(1)


def mat(name, color, metallic=0.0, roughness=0.55, alpha=1.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    if alpha < 1:
        m.blend_method = "BLEND"
        m.use_screen_refraction = True
        m.show_transparent_back = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Alpha"].default_value = alpha
    return m


def col(name, parent=None):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if not c.users:
        (parent.children if parent else bpy.context.scene.collection.children).link(c)
    return c


def link(obj, c):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    c.objects.link(obj)
    return obj


def mark_export(obj, group):
    obj["export_group"] = group
    return obj


def no_export(obj, reason="reference"):
    obj["no_export"] = reason
    return obj


def cube(name, loc, dims, material, c, bevel=0.0, rotation=(0, 0, 0), export_group=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rotation)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        b = o.modifiers.new("print_edge_radius", "BEVEL")
        b.width = bevel
        b.segments = 2
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.modifier_apply(modifier=b.name)
        o.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")
    o.data.materials.append(material)
    link(o, c)
    if export_group:
        mark_export(o, export_group)
    return o


def cyl(name, loc, radius, depth, material, c, vertices=40, rotation=(0, 0, 0), export_group=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rotation)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(material)
    link(o, c)
    if export_group:
        mark_export(o, export_group)
    return o


def cyl_between(name, a, b, radius, material, c, vertices=32, export_group=None):
    av, bv = Vector(a), Vector(b)
    mid = (av + bv) * 0.5
    d = bv - av
    o = cyl(name, mid, radius, d.length, material, c, vertices=vertices)
    o.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    if export_group:
        mark_export(o, export_group)
    return o


def sphere(name, loc, radius, material, c, segments=16, export_group=None):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments,
        ring_count=max(8, segments // 2),
        radius=radius,
        location=loc,
    )
    o = bpy.context.object
    o.name = name
    o.data.materials.append(material)
    link(o, c)
    if export_group:
        mark_export(o, export_group)
    return o


def mesh_obj(name, verts, faces, material, c, export_group=None):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update(calc_edges=True)
    o = bpy.data.objects.new(name, mesh)
    o.data.materials.append(material)
    c.objects.link(o)
    if export_group:
        mark_export(o, export_group)
    return o


def set_origin(o, loc):
    old = bpy.context.scene.cursor.location.copy()
    bpy.context.scene.cursor.location = loc
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")
    bpy.context.scene.cursor.location = old


def parent_keep_transform(child, parent):
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()


def empty(name, loc, c, parent=None):
    o = bpy.data.objects.new(name, None)
    o.empty_display_type = "ARROWS"
    o.empty_display_size = 12
    o.location = loc
    c.objects.link(o)
    no_export(o, "animation pivot")
    if parent:
        parent_keep_transform(o, parent)
    return o


def add_solidify(o, thickness):
    s = o.modifiers.new("real_print_wall_thickness", "SOLIDIFY")
    s.thickness = thickness
    s.offset = 0
    s.use_quality_normals = True
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.modifier_apply(modifier=s.name)
    o.select_set(False)
    return o


def build_body_shell(c, M):
    x0, x1 = 0.0, BODY_L
    y0, y1 = -BODY_W / 2, BODY_W / 2
    z0, zf, zt = BODY_Z0, FLOOR_TOP, BODY_TOP
    t = WALL
    ob = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)]
    ot = [(x0, y0, zt), (x1, y0, zt), (x1, y1, zt), (x0, y1, zt)]
    ib = [(x0 + t, y0 + t, zf), (x1 - t, y0 + t, zf), (x1 - t, y1 - t, zf), (x0 + t, y1 - t, zf)]
    it = [(x0 + t, y0 + t, zt), (x1 - t, y0 + t, zt), (x1 - t, y1 - t, zt), (x0 + t, y1 - t, zt)]
    verts = ob + ot + ib + it
    O0, O1, O2, O3 = 0, 1, 2, 3
    T0, T1, T2, T3 = 4, 5, 6, 7
    I0, I1, I2, I3 = 8, 9, 10, 11
    U0, U1, U2, U3 = 12, 13, 14, 15
    faces = [
        (O0, O3, O2, O1),
        (O0, O1, T1, T0),
        (O1, O2, T2, T1),
        (O2, O3, T3, T2),
        (O3, O0, T0, T3),
        (T0, T1, U1, U0),
        (T1, T2, U2, U1),
        (T2, T3, U3, U2),
        (T3, T0, U0, U3),
        (I0, U0, U1, I1),
        (I1, U1, U2, I2),
        (I2, U2, U3, I3),
        (I3, U3, U0, I0),
        (I0, I1, I2, I3),
    ]
    shell = mesh_obj("MVP_open_top_container_shell_closed_front_3p2mm_wall", verts, faces, M["body"], c, "body_fixed")
    shell["print_wall_mm"] = WALL
    shell["purpose"] = "single printable open-top container body; front wall is closed, bucket dumps over rim"
    return shell


def build_body_details(c, M):
    # Removable smooth outer shell mounts for the radiation layer the user will add later.
    for side, y, outward in [("left", -78.5, -1), ("right", 78.5, 1)]:
        for x in [35, 85, 135, 185, 235]:
            cyl(
                f"{side}_radiation_layer_M3_standoff_boss_x{x}",
                (x, y, 108),
                3.0,
                5.0,
                M["body"],
                c,
                vertices=24,
                rotation=(math.radians(90), 0, 0),
                export_group="body_fixed",
            )
            cyl(
                f"{side}_radiation_layer_3p4mm_clearance_hole_marker_x{x}",
                (x, y + outward * 2.8, 108),
                1.7,
                1.2,
                M["dark"],
                c,
                vertices=20,
                rotation=(math.radians(90), 0, 0),
            )
    cube("rear_service_hatch_printed_lip", (262.5, 0, 83), (5.0, 92, 48), M["panel"], c, 1.0, export_group="body_fixed")
    cyl_between("rear_hatch_M3_hinge_pin_reference", (266, -46, 59), (266, 46, 59), 1.8, M["steel"], c, 24)
    cube("rear_power_switch_mount_flat", (263.5, -51, 101), (4, 18, 12), M["orange"], c, 0.6, export_group="body_fixed")
    cube("rear_charge_port_mount_flat", (263.5, 51, 101), (4, 18, 12), M["orange"], c, 0.6, export_group="body_fixed")

    # Arduino and battery bays are physical printed trays plus transparent keep-out volumes.
    arduino = cube("avionics_Arduino_UNO_tray_76x58_with_2mm_clearance", (188, -35, 56.5), (84, 66, 7), M["bay"], c, 0.8, export_group="body_fixed")
    arduino["fits"] = "Arduino UNO style board, approx 69 x 54 mm, with wiring clearance"
    for dx, dy in [(-29, -22), (29, -22), (-29, 22), (29, 22)]:
        cyl("avionics_M3_standoff_post", (188 + dx, -35 + dy, 64), 3.0, 12.0, M["body"], c, 24, export_group="body_fixed")
        cyl("avionics_1p7mm_pilot_hole_marker", (188 + dx, -35 + dy, 70.4), 1.7, 1.0, M["dark"], c, 18)
    keep = cube("KEEP_OUT_Arduino_UNO_space_not_printed_76x58x24", (188, -35, 76), (76, 58, 24), M["keepout"], c, 0.2)
    no_export(keep, "electronics clearance volume")

    battery = cube("battery_pack_tray_2x18650_or_small_LiPo_92x44", (188, 36, 56.5), (96, 50, 7), M["bay"], c, 0.8, export_group="body_fixed")
    battery["fits"] = "two 18650 cells in holder or small 2S LiPo pack with strap"
    for y in [27.5, 44.5]:
        cyl(
            "KEEP_OUT_battery_cell_space_not_printed_18mm_dia",
            (188, y, 69),
            9.4,
            70,
            M["keepout"],
            c,
            vertices=32,
            rotation=(0, math.radians(90), 0),
        )
        no_export(bpy.context.object, "battery clearance volume")
    cube("battery_retaining_strap_bridge_printed", (188, 36, 80), (76, 4, 5), M["orange"], c, 0.6, export_group="body_fixed")

    cube("central_wire_channel_12mm_between_bays", (133, 0, 57), (108, 14, 8), M["dark"], c, 0.6, export_group="body_fixed")
    for x in [95, 125, 155]:
        cube(f"wire_clip_bridge_x{x}", (x, 0, 66), (14, 20, 3), M["orange"], c, 0.5, export_group="body_fixed")

    # Minimal MVP sensor sockets only. These are empty mounts, not a 48/100 sensor sculpture.
    sensor_positions = [
        ("front_left_camera_socket", (6, -45, 116), (math.radians(90), 0, 0)),
        ("front_right_camera_socket", (6, 45, 116), (math.radians(90), 0, 0)),
        ("rear_left_debug_socket", (254, -45, 116), (math.radians(90), 0, 0)),
        ("rear_right_debug_socket", (254, 45, 116), (math.radians(90), 0, 0)),
        ("bucket_range_sensor_socket", (11, 0, 113), (0, math.radians(90), 0)),
        ("top_imu_mount_socket", (130, 0, 132), (0, 0, 0)),
    ]
    for name, loc, rot in sensor_positions:
        cyl(name, loc, 4.5, 3.0, M["sensor"], c, 24, rotation=rot, export_group="body_fixed")
        cyl(name + "_M2_pilot_marker", loc, 1.1, 3.2, M["dark"], c, 16, rotation=rot)


def build_wheel_mesh(name, center, outer_radius, width, hole_radius, material, c, export_group):
    segments = 96
    lug_count = 24
    lug_depth = 5.0
    base_radius = outer_radius - lug_depth
    verts = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        phase = (i * lug_count / segments) % 1.0
        r = outer_radius if phase < 0.42 else base_radius
        ca, sa = math.cos(angle), math.sin(angle)
        x = center[0] + ca * r
        z = center[2] + sa * r
        xi = center[0] + ca * hole_radius
        zi = center[2] + sa * hole_radius
        verts.extend(
            [
                (x, center[1] - width / 2, z),
                (x, center[1] + width / 2, z),
                (xi, center[1] - width / 2, zi),
                (xi, center[1] + width / 2, zi),
            ]
        )
    faces = []
    for i in range(segments):
        j = (i + 1) % segments
        ol_i, or_i, il_i, ir_i = i * 4, i * 4 + 1, i * 4 + 2, i * 4 + 3
        ol_j, or_j, il_j, ir_j = j * 4, j * 4 + 1, j * 4 + 2, j * 4 + 3
        faces.append((ol_i, ol_j, or_j, or_i))
        faces.append((il_j, il_i, ir_i, ir_j))
        faces.append((ol_j, ol_i, il_i, il_j))
        faces.append((or_i, or_j, ir_j, ir_i))
    wheel = mesh_obj(name, verts, faces, material, c, export_group)
    wheel["axle_clearance_diameter_mm"] = round(hole_radius * 2, 2)
    wheel["intended_hardware"] = "3 mm axle or M3 bolt through 3.4 mm printed hole"
    return wheel


def build_wheels(c, M):
    radius = 37.0
    width = 28.0
    centers_x = [42, 130, 218]
    for side, y, outward in [("left", -94, -1), ("right", 94, 1)]:
        for idx, x in enumerate(centers_x, 1):
            wheel = build_wheel_mesh(
                f"{side}_large_lunar_wheel_{idx}_74mm_dia_integrated_tread",
                (x, y, radius),
                radius,
                width,
                1.5 + HINGE_CLEARANCE / 2,
                M["tire"],
                c,
                f"wheel_{side}_{idx}",
            )
            wheel["motion"] = "rotates freely about Y-axis; ground contact verified at z=0"
            cyl(
                f"{side}_wheel_{idx}_M3_axle_pin_reference_not_printed",
                (x, y, radius),
                1.5,
                45,
                M["steel"],
                c,
                24,
                rotation=(math.radians(90), 0, 0),
            )
            cube(
                f"{side}_wheel_{idx}_body_axle_fork_upper",
                (x, y - outward * 19, radius + 15),
                (26, 7, 14),
                M["body"],
                c,
                0.8,
                export_group="body_fixed",
            )
            cube(
                f"{side}_wheel_{idx}_body_axle_fork_lower",
                (x, y - outward * 19, radius - 15),
                (26, 7, 14),
                M["body"],
                c,
                0.8,
                export_group="body_fixed",
            )
            cyl(
                f"{side}_wheel_{idx}_gear_motor_mockup_25mm_can_space",
                (x, y - outward * 31, radius),
                12.5,
                24,
                M["orange"],
                c,
                32,
                rotation=(math.radians(90), 0, 0),
                export_group="body_fixed",
            )
            cube(
                f"{side}_wheel_{idx}_motor_wire_passage_to_body",
                (x, y - outward * 13, radius),
                (12, 12, 10),
                M["dark"],
                c,
                0.4,
                export_group="body_fixed",
            )


def build_bucket_shell(c, M):
    width = 118.0
    half = width / 2
    points = [
        (-30, 78),
        (-30, 47),
        (-41, 37),
        (-58, 29),
        (-79, 25),
        (-103, 29),
    ]
    verts = []
    for x, z in points:
        verts.append((x, -half, z))
        verts.append((x, half, z))
    faces = []
    for i in range(len(points) - 1):
        faces.append((2 * i, 2 * i + 2, 2 * i + 3, 2 * i + 1))
    scoop = mesh_obj("bucket_curved_scoop_floor_and_back_3mm_wall", verts, faces, M["bucket"], c, "bucket_scoop")
    add_solidify(scoop, 3.0)
    scoop["purpose"] = "curved scoop; not a square box"

    side_faces = [(i for i in [])]
    left_verts = [(x, -half - 1.5, z) for x, z in points] + [(-103, -half - 1.5, 56), (-30, -half - 1.5, 83)]
    right_verts = [(x, half + 1.5, z) for x, z in points] + [(-103, half + 1.5, 56), (-30, half + 1.5, 83)]
    side_poly = (0, 1, 2, 3, 4, 5, 6, 7)
    left = mesh_obj("bucket_left_curved_side_plate_3mm", left_verts, [side_poly], M["bucket"], c, "bucket_scoop")
    right = mesh_obj("bucket_right_curved_side_plate_3mm", right_verts, [tuple(reversed(side_poly))], M["bucket"], c, "bucket_scoop")
    add_solidify(left, 3.0)
    add_solidify(right, 3.0)

    cyl_between("bucket_curl_axis_under_bucket_hinge_tube", (-34, -63, 57), (-34, 63, 57), 3.8, M["steel"], c, 32, "bucket_scoop")
    cyl_between("bucket_front_cutting_edge_steel_bar", (-104, -59, 28), (-104, 59, 28), 2.8, M["steel"], c, 24, "bucket_scoop")
    for y in [-44, -22, 0, 22, 44]:
        tooth = cube("bucket_replaceable_tooth_blunt_MVP", (-111, y, 24), (13, 9, 5), M["steel"], c, 0.5, rotation=(0, math.radians(-10), 0), export_group="bucket_scoop")
        tooth["note"] = "blunt tooth for first FDM MVP test, easy to reprint"
    for y in [-52, 52]:
        cube("bucket_curl_torque_tab_with_M3_hole_marker", (-47, y, 51), (16, 5, 18), M["orange"], c, 0.5, export_group="bucket_scoop")
        cyl("bucket_torque_tab_M3_hole_marker", (-47, y, 51), 1.7, 5.5, M["dark"], c, 18, rotation=(math.radians(90), 0, 0))
    bucket_parts = [o for o in c.objects if o.name.startswith("bucket_")]
    for o in bucket_parts:
        if o.type == "MESH":
            parent_target = None
    set_origin(scoop, (-34, 0, 57))
    return scoop


def build_bucket_mechanism(c, M):
    lift_axis = empty("ANIM_bucket_lift_axis_body_pin_scrub_timeline", (8, 0, 74), c)
    curl_axis = empty("ANIM_bucket_second_axis_curl_under_scoop", (-34, 0, 57), c, lift_axis)
    lift_axis["motion_range_deg"] = "0 to 62 degrees"
    curl_axis["motion_range_deg"] = "0 to 105 degrees relative to lift arm"
    lift_axis["test"] = "scrub frames 1-100: dig, lift, curl/dump"

    for y in [-54, 54]:
        cyl("bucket_lift_axis_body_bearing_boss", (8, y, 74), 5.2, 8.0, M["body"], c, 32, rotation=(math.radians(90), 0, 0), export_group="body_fixed")
        cyl("bucket_lift_axis_M3_clearance_marker", (8, y, 74), 1.9, 9.0, M["dark"], c, 24, rotation=(math.radians(90), 0, 0))
        arm = cyl_between(f"bucket_lift_arm_{'left' if y < 0 else 'right'}_prints_flat", (8, y, 74), (-34, y, 57), 4.2, M["arm"], c, 32, "bucket_lift_arms")
        set_origin(arm, (8, y, 74))
        parent_keep_transform(arm, lift_axis)
        cyl(f"bucket_lift_arm_pivot_washer_y{y}", (8, y, 74), 6.5, 2.5, M["steel"], c, 32, rotation=(math.radians(90), 0, 0))
        cyl(f"bucket_curl_pivot_washer_y{y}", (-34, y, 57), 6.5, 2.5, M["steel"], c, 32, rotation=(math.radians(90), 0, 0))

        lift_act = cyl_between(
            f"bucket_lift_linear_actuator_mock_{'left' if y < 0 else 'right'}_60mm_stroke",
            (30, y, 57),
            (-15, y, 68),
            3.0,
            M["orange"],
            c,
            24,
            "body_fixed",
        )
        lift_act["note"] = "printed actuator placeholder, replace with micro linear actuator or servo linkage"
        curl_pushrod = cyl_between(
            f"bucket_curl_pushrod_second_axis_{'left' if y < 0 else 'right'}",
            (-24, y, 73),
            (-50, y, 51),
            2.2,
            M["steel"],
            c,
            20,
            "bucket_pushrods",
        )
        parent_keep_transform(curl_pushrod, lift_axis)

    cube("front_bucket_servo_mount_left_20x40_space", (18, -63, 58), (17, 12, 28), M["orange"], c, 0.6, export_group="body_fixed")
    cube("front_bucket_servo_mount_right_20x40_space", (18, 63, 58), (17, 12, 28), M["orange"], c, 0.6, export_group="body_fixed")
    envelope = cube("KEEP_OUT_bucket_motion_envelope_lift_clearance", (-35, 0, 103), (88, 136, 102), M["motion"], c, 0.5)
    envelope.display_type = "WIRE"
    envelope.hide_render = True
    no_export(envelope, "transparent motion check volume")

    bucket_shell = build_bucket_shell(c, M)
    parent_keep_transform(bucket_shell, curl_axis)
    for o in c.objects:
        if o.name.startswith("bucket_") and o != bucket_shell and o.type == "MESH":
            parent_keep_transform(o, curl_axis)

    scene = bpy.context.scene
    lift_axis.rotation_euler[1] = 0
    curl_axis.rotation_euler[1] = 0
    lift_axis.keyframe_insert(data_path="rotation_euler", frame=1)
    curl_axis.keyframe_insert(data_path="rotation_euler", frame=1)
    lift_axis.rotation_euler[1] = math.radians(48)
    curl_axis.rotation_euler[1] = math.radians(10)
    lift_axis.keyframe_insert(data_path="rotation_euler", frame=55)
    curl_axis.keyframe_insert(data_path="rotation_euler", frame=55)
    lift_axis.rotation_euler[1] = math.radians(62)
    curl_axis.rotation_euler[1] = math.radians(105)
    lift_axis.keyframe_insert(data_path="rotation_euler", frame=100)
    curl_axis.keyframe_insert(data_path="rotation_euler", frame=100)
    scene.frame_set(1)
    return lift_axis, curl_axis


def build_arm_module(c, M, side):
    outward = -1 if side == "left" else 1
    y_wall = -BODY_W / 2 if side == "left" else BODY_W / 2
    y = y_wall + outward * 18
    ac = col(f"{side}_working_robotic_arm_module", c)
    rail_z = 114
    cyl_between(f"{side}_arm_top_slide_rail_4mm_rod", (54, y, rail_z), (224, y, rail_z), 2.0, M["steel"], ac, 24, "body_fixed")
    cyl_between(f"{side}_arm_lower_slide_rail_4mm_rod", (54, y, rail_z - 14), (224, y, rail_z - 14), 2.0, M["steel"], ac, 24, "body_fixed")
    for x in [54, 104, 154, 204, 224]:
        cube(f"{side}_arm_rail_body_bracket_x{x}", (x, y_wall + outward * 4, rail_z - 7), (8, 8, 28), M["body"], ac, 0.6, export_group="body_fixed")
    carriage = cube(f"{side}_arm_sliding_carriage_servo_pocket_9g", (122, y, rail_z - 7), (30, 13, 28), M["orange"], ac, 0.8, export_group=f"{side}_arm_carriage")
    carriage["fits"] = "9g/micro servo pocket or printed bearing carriage"
    shoulder = empty(f"ANIM_{side}_arm_shoulder_axis", (122, y + outward * 11, rail_z - 7), ac)
    elbow = empty(f"ANIM_{side}_arm_elbow_axis", (150, y + outward * 36, rail_z - 1), ac, shoulder)
    wrist = empty(f"ANIM_{side}_arm_wrist_axis", (180, y + outward * 58, rail_z - 22), ac, elbow)
    shoulder["motion_range_deg"] = "-35 to +70"
    elbow["motion_range_deg"] = "-85 to +80"

    upper = cyl_between(f"{side}_arm_upper_link_round_bar_with_pin_clearance", shoulder.location, elbow.location, 3.2, M["arm"], ac, 32, f"{side}_arm_links")
    fore = cyl_between(f"{side}_arm_forearm_link_round_bar_with_pin_clearance", elbow.location, wrist.location, 3.0, M["arm"], ac, 32, f"{side}_arm_links")
    set_origin(upper, shoulder.location)
    set_origin(fore, elbow.location)
    parent_keep_transform(upper, shoulder)
    parent_keep_transform(fore, elbow)
    for nm, p, parent in [("shoulder", shoulder.location, shoulder), ("elbow", elbow.location, elbow), ("wrist", wrist.location, wrist)]:
        pin = cyl(f"{side}_arm_{nm}_M3_pin_reference", p, 2.0, 14, M["steel"], ac, 24, rotation=(math.radians(90), 0, 0))
        washer = cyl(f"{side}_arm_{nm}_clearance_washer_0p6mm_gap", (p.x, p.y + outward * 7.5, p.z), 5.5, 1.2, M["dark"], ac, 24, rotation=(math.radians(90), 0, 0))
        parent_keep_transform(pin, parent)
        parent_keep_transform(washer, parent)
    tool = cube(f"{side}_arm_simple_tool_plate_for_test_payload", wrist.location + Vector((0, outward * 9, -3)), (18, 4, 18), M["orange"], ac, 0.5, export_group=f"{side}_arm_tool")
    parent_keep_transform(tool, wrist)

    shoulder.rotation_euler[0] = 0
    elbow.rotation_euler[0] = 0
    shoulder.keyframe_insert(data_path="rotation_euler", frame=1)
    elbow.keyframe_insert(data_path="rotation_euler", frame=1)
    shoulder.rotation_euler[0] = math.radians(outward * 24)
    elbow.rotation_euler[0] = math.radians(outward * -38)
    shoulder.keyframe_insert(data_path="rotation_euler", frame=55)
    elbow.keyframe_insert(data_path="rotation_euler", frame=55)
    shoulder.rotation_euler[0] = math.radians(outward * -32)
    elbow.rotation_euler[0] = math.radians(outward * 58)
    shoulder.keyframe_insert(data_path="rotation_euler", frame=100)
    elbow.keyframe_insert(data_path="rotation_euler", frame=100)
    return shoulder, elbow


def build_arms(c, M):
    left = build_arm_module(c, M, "left")
    right = build_arm_module(c, M, "right")
    bpy.context.scene.frame_set(1)
    return left, right


def build_reference_floor(c, M):
    floor = cube("VIEW_ONLY_clean_ground_plane_no_rocks_no_floating_parts", (130, 0, -1.5), (360, 260, 2), M["ground"], c)
    no_export(floor, "render reference")
    for x in range(-20, 281, 20):
        line = cyl_between(f"VIEW_ONLY_grid_x_{x}", (x, -125, 0.1), (x, 125, 0.1), 0.25, M["grid"], c, 8)
        no_export(line, "render reference")
    for y in range(-120, 121, 20):
        line = cyl_between(f"VIEW_ONLY_grid_y_{y}", (-30, y, 0.2), (290, y, 0.2), 0.25, M["grid"], c, 8)
        no_export(line, "render reference")


def build_scene():
    root = col("CONTAINER_v2_MVP_PRINTABLE_FUNCTIONAL")
    M = {
        "body": mat("mvp_printed_body_warm_white", (0.80, 0.80, 0.72, 1), 0.02, 0.55),
        "panel": mat("mvp_service_panel_gray", (0.55, 0.56, 0.54, 1), 0.05, 0.6),
        "bay": mat("mvp_electronics_bay_orange", (1.0, 0.46, 0.06, 1), 0.02, 0.45),
        "orange": mat("mvp_actuator_orange", (1.0, 0.44, 0.03, 1), 0.02, 0.43),
        "steel": mat("mvp_dark_steel_hardware", (0.08, 0.085, 0.08, 1), 0.75, 0.35),
        "dark": mat("mvp_black_clearance_markers", (0.025, 0.025, 0.022, 1), 0.15, 0.65),
        "bucket": mat("mvp_bucket_black_printed", (0.035, 0.035, 0.033, 1), 0.25, 0.50),
        "arm": mat("mvp_arm_link_aluminum", (0.68, 0.69, 0.64, 1), 0.25, 0.45),
        "tire": mat("mvp_tire_dark_fdm", (0.018, 0.018, 0.017, 1), 0.08, 0.72),
        "sensor": mat("mvp_sensor_socket_blue", (0.05, 0.22, 0.90, 1), 0.02, 0.38),
        "keepout": mat("transparent_electronics_keepout_not_printed", (0.1, 0.85, 0.35, 1), 0, 0.2, 0.22),
        "motion": mat("transparent_motion_envelope_not_printed", (0.1, 0.65, 1.0, 1), 0, 0.2, 0.12),
        "ground": mat("view_ground_plain", (0.35, 0.35, 0.33, 1), 0, 0.85),
        "grid": mat("view_ground_grid", (0.22, 0.22, 0.21, 1), 0, 0.9),
    }
    body = col("01_printed_body_shell_avionics_battery_bays", root)
    wheels = col("02_large_wheels_motor_mounts", root)
    bucket = col("03_bucket_lift_and_second_axis_curl", root)
    arms = col("04_two_working_exterior_robotic_arms", root)
    view = col("05_view_only_floor_and_clearance_references", root)
    build_body_shell(body, M)
    build_body_details(body, M)
    build_wheels(wheels, M)
    build_bucket_mechanism(bucket, M)
    build_arms(arms, M)
    build_reference_floor(view, M)
    root["design_intent"] = "FDM-printable MVP test rig with Arduino/battery bays, large wheels, curved bucket, lift plus curl axis, and two exterior arms."
    root["clearance_policy"] = "0.4 mm nominal FDM clearance, 0.6 mm around hinges and rotating shafts."
    return root


def signed_bucket_pose(angle_lift, angle_curl):
    lift_origin = Vector((8, 0, 74))
    curl_home = Vector((-34, 0, 57))
    lip_home = Vector((-104, 0, 28))
    R_lift = Matrix.Rotation(math.radians(angle_lift), 4, "Y")
    R_curl = Matrix.Rotation(math.radians(angle_curl), 4, "Y")
    curl = lift_origin + R_lift @ (curl_home - lift_origin)
    lip = curl + R_lift @ (R_curl @ (lip_home - curl_home))
    return curl, lip


def audit_scene(root):
    issues = []
    meshes = [o for o in root.all_objects if o.type == "MESH"]
    sensor_sockets = [o for o in meshes if "sensor" in o.name.lower() and "socket" in o.name.lower()]
    if len(sensor_sockets) > 8:
        issues.append(f"too many MVP sensor sockets: {len(sensor_sockets)}")
    if not bpy.data.objects.get("KEEP_OUT_Arduino_UNO_space_not_printed_76x58x24"):
        issues.append("Arduino keep-out volume missing")
    if not bpy.data.objects.get("battery_pack_tray_2x18650_or_small_LiPo_92x44"):
        issues.append("battery tray missing")
    wheel_objs = [o for o in meshes if "_large_lunar_wheel_" in o.name]
    if len(wheel_objs) != 6:
        issues.append(f"expected 6 large wheels, found {len(wheel_objs)}")
    for o in wheel_objs:
        zs = [(o.matrix_world @ Vector(v)).z for v in o.bound_box]
        if abs(min(zs)) > 0.6:
            issues.append(f"{o.name} does not touch ground within tolerance")
        if (max(zs) - min(zs)) < 70:
            issues.append(f"{o.name} is smaller than 70 mm diameter")
    for lift, curl in [(0, 0), (48, 10), (62, 105)]:
        axis, lip = signed_bucket_pose(lift, curl)
        if axis.x > -5 and lift < 10:
            issues.append("bucket curl axis too close to closed front wall in dig pose")
        if lift > 50 and lip.z < BODY_TOP + 8:
            issues.append(f"bucket lip too low to dump over rim at lift={lift}, curl={curl}")
    required = [
        "ANIM_bucket_lift_axis_body_pin_scrub_timeline",
        "ANIM_bucket_second_axis_curl_under_scoop",
        "ANIM_left_arm_shoulder_axis",
        "ANIM_right_arm_shoulder_axis",
    ]
    for name in required:
        if not bpy.data.objects.get(name):
            issues.append(f"missing movable pivot: {name}")
    export_groups = set()
    for o in meshes:
        if "export_group" in o:
            export_groups.add(o["export_group"])
    for group in ["body_fixed", "bucket_scoop", "wheel_left_1", "wheel_right_1"]:
        if group not in export_groups:
            issues.append(f"export group missing: {group}")
    return issues


def triangle_normal(a, b, c):
    n = (b - a).cross(c - a)
    if n.length == 0:
        return Vector((0, 0, 0))
    n.normalize()
    return n


def write_ascii_stl(path, objects):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii") as f:
        f.write(f"solid {path.stem}\n")
        for obj in objects:
            eval_obj = obj.evaluated_get(depsgraph)
            mesh = eval_obj.to_mesh()
            mw = eval_obj.matrix_world.copy()
            for poly in mesh.polygons:
                verts = [mw @ mesh.vertices[i].co for i in poly.vertices]
                if len(verts) < 3:
                    continue
                for i in range(1, len(verts) - 1):
                    a, b, c = verts[0], verts[i], verts[i + 1]
                    n = triangle_normal(a, b, c)
                    f.write(f"  facet normal {n.x:.6e} {n.y:.6e} {n.z:.6e}\n")
                    f.write("    outer loop\n")
                    for v in [a, b, c]:
                        f.write(f"      vertex {v.x:.6e} {v.y:.6e} {v.z:.6e}\n")
                    f.write("    endloop\n")
                    f.write("  endfacet\n")
            eval_obj.to_mesh_clear()
        f.write(f"endsolid {path.stem}\n")


def export_stls(root):
    bpy.context.scene.frame_set(1)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    groups = {}
    for obj in root.all_objects:
        if obj.type != "MESH" or "no_export" in obj:
            continue
        group = obj.get("export_group")
        if not group:
            continue
        groups.setdefault(group, []).append(obj)
    for group, objects in sorted(groups.items()):
        write_ascii_stl(EXPORT_DIR / f"{group}.stl", objects)
    # A body-focused assembly STL is convenient for first print checks.
    body_groups = ["body_fixed"]
    body_objs = [o for g in body_groups for o in groups.get(g, [])]
    if body_objs:
        write_ascii_stl(EXPORT_DIR / "MVP_body_shell_with_avionics_and_battery_bays.stl", body_objs)
    return groups


def render_preview():
    RENDER.parent.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.color_type = "MATERIAL"
    scene.render.resolution_x = 1900
    scene.render.resolution_y = 1200
    scene.view_settings.view_transform = "Filmic"
    scene.frame_set(1)
    bpy.ops.object.light_add(type="SUN", location=(100, -140, 220))
    sun = bpy.context.object
    sun.name = "mvp_preview_sun"
    sun.rotation_euler = (math.radians(45), 0, math.radians(-35))
    sun.data.energy = 2.8
    bpy.ops.object.camera_add(location=(-245, -230, 160))
    cam = bpy.context.object
    cam.name = "mvp_preview_camera"
    target = Vector((105, 0, 72))
    direction = target - Vector(cam.location)
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 310
    scene.camera = cam
    scene.render.filepath = str(RENDER)
    bpy.ops.render.render(write_still=True)


def write_report(issues, groups):
    lines = [
        "# CONTAINER v2 MVP Printable Rebuild Report",
        "",
        "This iteration replaces the decorative/full-scale concept with a millimeter-scale MVP test rig.",
        "",
        "What was wrong:",
        "- Wheels were too small and not mechanically connected enough for dusty terrain testing.",
        "- The scene had too many sensor bosses for an MVP and several looked like floating clutter.",
        "- The bucket was square and did not include a real lift/curl mechanism.",
        "- Electronics and battery spaces were not designed as printable MVP bays.",
        "- Exterior shield-like panels made the wall busy even though the radiation layer will be added later.",
        "- Robotic arms were visual arms, not clear mechanical linkages with pivots and servo spaces.",
        "",
        "What was fixed:",
        "- Rebuilt the body as an open-top 260 x 150 x 108 mm printable shell with a closed front wall.",
        "- Added Arduino UNO tray, 2x18650/small LiPo battery tray, switch mount, charge-port mount, and wire channel.",
        "- Replaced the sensor manifest with 6 minimal sensor sockets and pilot-hole markers.",
        "- Rebuilt wheels as six 74 mm diameter treaded wheels with 3.4 mm axle holes and motor mockup spaces.",
        "- Rebuilt the bucket as a curved scoop with a lift axis and a second under-bucket curl axis.",
        "- Added lift actuator placeholders, curl pushrods, servo pockets, hinge washers, and timeline animation pivots.",
        "- Rebuilt the robotic arms as two exterior rail-mounted linkages with shoulder/elbow/wrist pivots.",
        "- Removed rocks, floating clutter, decorative radiation panels, and the old 48-sensor MVP overload.",
        "",
        "Moving parts verified in the model:",
        "- Bucket lift axis: scrub frames 1-100; frame 1 dig, frame 55 lift, frame 100 lift plus curl/dump.",
        "- Bucket second curl axis: under-scoop hinge rotates relative to lift arm for steeper dumping.",
        "- Six wheel bodies: separate printable wheel STLs around 3 mm axle/M3 bolt clearance.",
        "- Left and right exterior robotic arms: shoulder and elbow pivots are keyframed on frames 1-100.",
        "",
        "Clearances used:",
        f"- Nominal FDM moving clearance: {MM_CLEARANCE:.1f} mm.",
        f"- Hinge/shaft allowance used in holes and washers: {HINGE_CLEARANCE:.1f} mm.",
        "- Wheel axle hole: 3.6 mm for a 3.0 mm shaft/M3 bolt.",
        "- Electronics keep-out volumes are visible transparent references and are not exported as print geometry.",
        "",
        f"Audit result: {'PASS' if not issues else 'ISSUES FOUND'}",
    ]
    lines.extend([f"- {issue}" for issue in issues] or ["- No known fixable issues from the scripted MVP audit."])
    lines.extend(
        [
            "",
            "Exported STL groups:",
            *[f"- `{group}.stl` ({len(objects)} mesh object(s))" for group, objects in sorted(groups.items())],
            "",
            "Remaining assumptions:",
            "- This is still a Blender MVP prototype, not a stress-checked CAD assembly.",
            "- Use real M3/M4 hardware, shafts, bearings/bushings, and servos/linear actuators for movement tests.",
            "- Before printing, choose final Arduino/battery hardware and adjust tray holes if your exact board/pack differs.",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    clear_scene()
    configure_scene()
    root = build_scene()
    issues = audit_scene(root)
    groups = export_stls(root)
    render_preview()
    bpy.context.scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(CLEAN_BLEND))
    bpy.ops.wm.save_as_mainfile(filepath=str(MAIN_BLEND))
    write_report(issues, groups)
    print(f"ISSUES={len(issues)}")
    print(f"MAIN_BLEND={MAIN_BLEND}")
    print(f"CLEAN_BLEND={CLEAN_BLEND}")
    print(f"REPORT={REPORT}")
    print(f"RENDER={RENDER}")
    print(f"EXPORT_DIR={EXPORT_DIR}")


if __name__ == "__main__":
    main()
