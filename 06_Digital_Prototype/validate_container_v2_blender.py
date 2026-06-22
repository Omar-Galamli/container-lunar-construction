from pathlib import Path
import traceback
import re

import bpy


ROOT = Path(__file__).resolve().parents[1]
BLEND_PATH = ROOT / "06_Digital_Prototype" / "CONTAINER_v2_Blender_Prototype.blend"
RENDER_DIR = ROOT / "06_Digital_Prototype" / "renders"
REPORT_PATH = ROOT / "06_Digital_Prototype" / "CONTAINER_v2_Blender_Prototype_validation.txt"


def fail(message):
    raise AssertionError(message)


def close_enough(value, expected, tolerance=0.03):
    return abs(value - expected) <= tolerance


def main():
    bpy.ops.wm.open_mainfile(filepath=str(BLEND_PATH))
    required_collections = [
        "Body_Open_Regolith_Bin",
        "Protected_Underfloor_Deck",
        "Front_Sliding_Lift_Bucket",
        "Side_Rail_Arms",
        "Sensors_48_Manifest",
        "Shielding_Thermal_Service",
        "Provisional_Mobility_REFERENCE_ONLY",
        "Lunar_Context",
        "Pose_States",
    ]
    missing = [name for name in required_collections if name not in bpy.data.collections]
    if missing:
        fail(f"Missing collections: {missing}")

    body_objects = [
        bpy.data.objects["fixed_body_left_wall_8m"],
        bpy.data.objects["fixed_body_right_wall_8m"],
        bpy.data.objects["fixed_body_front_wall_bucket_opening"],
        bpy.data.objects["fixed_body_rear_service_wall"],
    ]
    min_x = min(obj.bound_box[i][0] * obj.scale.x + obj.location.x for obj in body_objects for i in range(8))
    max_x = max(obj.bound_box[i][0] * obj.scale.x + obj.location.x for obj in body_objects for i in range(8))
    min_y = min(obj.bound_box[i][1] * obj.scale.y + obj.location.y for obj in body_objects for i in range(8))
    max_y = max(obj.bound_box[i][1] * obj.scale.y + obj.location.y for obj in body_objects for i in range(8))
    min_z = min(obj.bound_box[i][2] * obj.scale.z + obj.location.z for obj in body_objects for i in range(8))
    max_z = max(obj.bound_box[i][2] * obj.scale.z + obj.location.z for obj in body_objects for i in range(8))
    if not close_enough(max_x - min_x, 8.0, 0.20):
        fail(f"Body length not near 8 m: {max_x - min_x}")
    if not close_enough(max_y - min_y, 6.0, 0.20):
        fail(f"Body width not near 6 m: {max_y - min_y}")
    if not close_enough(max_z - min_z, 4.0, 0.20):
        fail(f"Body height not near 4 m: {max_z - min_z}")

    floor = bpy.data.objects["raised_internal_floor_Z0900"]
    if not close_enough(floor.location.z, 0.9, 0.02):
        fail(f"Raised floor not at Z=0.9 m: {floor.location.z}")

    rail = bpy.data.objects["left_arm_rail_X0800_X7200_Z3150"]
    if not close_enough(rail.location.z, 3.15, 0.05):
        fail(f"Arm rail not near Z=3.15 m: {rail.location.z}")

    sensor_count = len([obj for obj in bpy.data.collections["Sensors_48_Manifest"].objects if obj.name.startswith("S")])
    if sensor_count < 48:
        fail(f"Expected at least 48 sensor markers, found {sensor_count}")

    prohibited_patterns = [
        r"(^|_)gantry($|_)",
        r"(^|_)anchor($|_)",
        r"(^|_)outrigger($|_)",
        r"(^|_)stabilizer($|_)",
        r"(^|_)leveling($|_)",
        r"(^|_)roof($|_)",
        r"(^|_)lid($|_)",
    ]
    bad_names = [
        obj.name
        for obj in bpy.data.objects
        if any(re.search(pattern, obj.name.lower()) for pattern in prohibited_patterns)
    ]
    if bad_names:
        fail(f"Prohibited v1 system names found: {bad_names}")

    required_renders = [
        "front_left_perspective.png",
        "top_orthographic.png",
        "right_side_elevation.png",
        "rear_service_view.png",
        "bucket_arm_detail_view.png",
    ]
    missing_renders = [name for name in required_renders if not (RENDER_DIR / name).exists()]
    if missing_renders:
        fail(f"Missing renders: {missing_renders}")

    REPORT_PATH.write_text(
        "\n".join(
            [
                "CONTAINER v2 Blender prototype validation: PASS",
                f"Collections checked: {len(required_collections)}",
                f"Sensor markers found: {sensor_count}",
                f"Body envelope approx: {max_x - min_x:.2f} x {max_y - min_y:.2f} x {max_z - min_z:.2f} m",
                f"Raised floor Z: {floor.location.z:.2f} m",
                f"Arm rail Z: {rail.location.z:.2f} m",
                f"Renders checked: {len(required_renders)}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        REPORT_PATH.write_text(traceback.format_exc(), encoding="utf-8")
        raise
