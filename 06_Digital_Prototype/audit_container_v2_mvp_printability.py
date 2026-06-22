import json
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "06_Digital_Prototype"
BLEND = OUT_DIR / "CONTAINER_v2_Blender_Prototype.blend"
EXPORT_DIR = OUT_DIR / "exports_mvp_printable"
OUT_JSON = OUT_DIR / "CONTAINER_v2_mvp_printability_audit.json"
OUT_MD = OUT_DIR / "CONTAINER_v2_mvp_printability_audit.md"


def bbox(obj):
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    return {
        "min": [round(min(getattr(p, a) for p in pts), 3) for a in "xyz"],
        "max": [round(max(getattr(p, a) for p in pts), 3) for a in "xyz"],
    }


def edge_face_counts(mesh):
    counts = {}
    for poly in mesh.polygons:
        verts = list(poly.vertices)
        for i, a in enumerate(verts):
            b = verts[(i + 1) % len(verts)]
            key = tuple(sorted((a, b)))
            counts[key] = counts.get(key, 0) + 1
    return counts


def audit_mesh(obj, depsgraph):
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()
    counts = edge_face_counts(mesh)
    nonmanifold = sum(1 for count in counts.values() if count != 2)
    zero_area_faces = 0
    for poly in mesh.polygons:
        if poly.area < 0.000001:
            zero_area_faces += 1
    result = {
        "name": obj.name,
        "verts": len(mesh.vertices),
        "faces": len(mesh.polygons),
        "nonmanifold_edges": nonmanifold,
        "zero_area_faces": zero_area_faces,
        "export_group": obj.get("export_group", ""),
        "bbox": bbox(obj),
    }
    eval_obj.to_mesh_clear()
    return result


def main():
    bpy.ops.wm.open_mainfile(filepath=str(BLEND))
    bpy.context.scene.frame_set(1)
    root = bpy.data.collections.get("CONTAINER_v2_MVP_PRINTABLE_FUNCTIONAL")
    objects = list(root.all_objects) if root else list(bpy.context.scene.objects)
    meshes = [o for o in objects if o.type == "MESH"]
    export_meshes = [o for o in meshes if o.get("export_group") and "no_export" not in o]
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh_results = [audit_mesh(o, depsgraph) for o in export_meshes]
    stls = sorted(EXPORT_DIR.glob("*.stl"))
    sensor_sockets = [
        o.name
        for o in meshes
        if (
            "socket" in o.name.lower()
            and "marker" not in o.name.lower()
            and any(token in o.name.lower() for token in ["camera", "debug", "sensor", "imu"])
        )
    ]
    wheel_results = []
    for wheel in [o for o in meshes if "_large_lunar_wheel_" in o.name]:
        b = bbox(wheel)
        wheel_results.append(
            {
                "name": wheel.name,
                "diameter_z_mm": round(b["max"][2] - b["min"][2], 3),
                "ground_gap_mm": round(b["min"][2], 3),
                "axle_clearance_diameter_mm": wheel.get("axle_clearance_diameter_mm"),
            }
        )
    issues = []
    for r in mesh_results:
        if r["nonmanifold_edges"]:
            issues.append(f"{r['name']} has {r['nonmanifold_edges']} non-manifold edges")
        if r["zero_area_faces"]:
            issues.append(f"{r['name']} has {r['zero_area_faces']} zero-area faces")
    if len(sensor_sockets) > 8:
        issues.append(f"MVP has too many sensor sockets: {len(sensor_sockets)}")
    for r in wheel_results:
        if r["diameter_z_mm"] < 70:
            issues.append(f"{r['name']} is under 70 mm diameter")
        if abs(r["ground_gap_mm"]) > 0.6:
            issues.append(f"{r['name']} ground gap is {r['ground_gap_mm']} mm")
    if not stls:
        issues.append("No STL files exported")
    report = {
        "blend": str(BLEND),
        "mesh_count": len(meshes),
        "export_mesh_count": len(export_meshes),
        "sensor_socket_count": len(sensor_sockets),
        "sensor_sockets": sensor_sockets,
        "wheel_checks": wheel_results,
        "stl_count": len(stls),
        "stls": [{"name": p.name, "bytes": p.stat().st_size} for p in stls],
        "mesh_results": mesh_results,
        "issues": issues,
    }
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    OUT_MD.write_text(
        "\n".join(
            [
                "# CONTAINER v2 MVP Printability Audit",
                "",
                f"Blend: `{BLEND}`",
                f"Export mesh count: {len(export_meshes)}",
                f"STL count: {len(stls)}",
                f"Sensor sockets: {len(sensor_sockets)}",
                "",
                "Wheel checks:",
                *[
                    f"- {r['name']}: diameter {r['diameter_z_mm']} mm, ground gap {r['ground_gap_mm']} mm, axle clearance {r['axle_clearance_diameter_mm']} mm"
                    for r in wheel_results
                ],
                "",
                f"Result: {'PASS' if not issues else 'ISSUES'}",
                *([f"- {issue}" for issue in issues] if issues else ["- No non-manifold, zero-area, wheel ground-contact, sensor-count, or STL export issues found in this audit."]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"ISSUES={len(issues)}")
    print(f"JSON={OUT_JSON}")
    print(f"MD={OUT_MD}")


if __name__ == "__main__":
    main()
