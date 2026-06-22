# CONTAINER v2 Printability and Motion Repair Report

- Repaired blend: `CONTAINER_v2_Blender_Prototype_REPAIRED_PRINTABLE.blend`
- Export directory: `exports_printable/`
- Printable scale: 1:40, giving an approximate body footprint of 200 mm x 150 mm.
- Nominal moving/separate-part clearance: 0.4 mm.
- Nominal structural wall thickness: 2.0 mm.

## Pre-repair issues found
- [high] The named front bucket opening is a solid wall, so the bucket dump path is blocked.
- [medium] Bucket primitives do not share a hinge origin, so curl motion cannot be tested as one part.
- [medium] Bucket tooth scaling is not applied, which is unsafe for export and downstream booleans.
- [high] Reference wheel modules intersect body side walls; wheel rotation is blocked.
- [high] Static arm links or carriages intersect the side walls; rail travel and arm swing are not clearanced.
- [low] Scene labels and datum helpers are useful references but should be excluded from print exports.
- [medium] Some existing meshes have non-manifold edge counts and should not be exported as-is.
- [medium] Original model has hidden pose-state duplicates instead of editable constrained moving assemblies.
- [medium] Original model has no export-only printable collection or per-part STL outputs.

## Post-repair motion and print checks
- [pass] printable body envelope (size_mm=[202.0, 152.0, 102.0], expected_mm_about=[200.0, 150.0, 102.0])
- [pass] bucket lateral slide (y_mm=39.15)
- [pass] bucket lateral slide (y_mm=75.0)
- [pass] bucket lateral slide (y_mm=110.85)
- [pass] bucket vertical lift (z_mm=22.5)
- [pass] bucket vertical lift (z_mm=52.5)
- [pass] bucket vertical lift (z_mm=82.5)
- [pass] bucket curl (angle_deg=-20)
- [pass] bucket curl (angle_deg=0)
- [pass] bucket curl (angle_deg=70)
- [pass] rear hatch swing (angle_deg=0)
- [pass] rear hatch swing (angle_deg=45)
- [pass] rear hatch swing (angle_deg=95)
- [pass] arm rail carriage travel (arm=A1_LF, x_mm=20.4)
- [pass] arm rail carriage travel (arm=A1_LF, x_mm=100.0)
- [pass] arm rail carriage travel (arm=A1_LF, x_mm=179.6)
- [pass] arm home wall clearance (arm=A1_LF, link=1)
- [pass] arm home wall clearance (arm=A1_LF, link=2)
- [pass] arm home wall clearance (arm=A1_LF, link=3)
- [pass] arm rail carriage travel (arm=A2_LR, x_mm=20.4)
- [pass] arm rail carriage travel (arm=A2_LR, x_mm=100.0)
- [pass] arm rail carriage travel (arm=A2_LR, x_mm=179.6)
- [pass] arm home wall clearance (arm=A2_LR, link=1)
- [pass] arm home wall clearance (arm=A2_LR, link=2)
- [pass] arm home wall clearance (arm=A2_LR, link=3)
- [pass] arm rail carriage travel (arm=A3_RF, x_mm=20.4)
- [pass] arm rail carriage travel (arm=A3_RF, x_mm=100.0)
- [pass] arm rail carriage travel (arm=A3_RF, x_mm=179.6)
- [pass] arm home wall clearance (arm=A3_RF, link=1)
- [pass] arm home wall clearance (arm=A3_RF, link=2)
- [pass] arm home wall clearance (arm=A3_RF, link=3)
- [pass] arm rail carriage travel (arm=A4_RR, x_mm=20.4)
- [pass] arm rail carriage travel (arm=A4_RR, x_mm=100.0)
- [pass] arm rail carriage travel (arm=A4_RR, x_mm=179.6)
- [pass] arm home wall clearance (arm=A4_RR, link=1)
- [pass] arm home wall clearance (arm=A4_RR, link=2)
- [pass] arm home wall clearance (arm=A4_RR, link=3)
- [pass] wheel rotation envelope (wheel=PRINT_left_wheel_1_rotating_clearanced)
- [pass] wheel rotation envelope (wheel=PRINT_left_wheel_2_rotating_clearanced)
- [pass] wheel rotation envelope (wheel=PRINT_left_wheel_3_rotating_clearanced)
- [pass] wheel rotation envelope (wheel=PRINT_left_wheel_4_rotating_clearanced)
- [pass] wheel rotation envelope (wheel=PRINT_right_wheel_1_rotating_clearanced)
- [pass] wheel rotation envelope (wheel=PRINT_right_wheel_2_rotating_clearanced)
- [pass] wheel rotation envelope (wheel=PRINT_right_wheel_3_rotating_clearanced)
- [pass] wheel rotation envelope (wheel=PRINT_right_wheel_4_rotating_clearanced)
- [pass] printable mesh manifold audit (objects_checked=114, non_manifold_count=0)
- [pass] minimum feature audit (minimum_feature_mm=1.2, below_threshold_count=0)

## Remaining limitations
- No known fixable motion or printability blockers remain in the printable collection.

## Exported STLs
- 114 STL files written.
