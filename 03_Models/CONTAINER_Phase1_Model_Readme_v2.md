# CONTAINER Phase 1 Model Readme v2

Date: 2026-06-15
Status: v2 model transition note

## Purpose

The original Phase 1 model remains preserved in `container_phase1_model.py` and `CONTAINER_Phase1_Model_Readme.md`. That model is a useful v1 reference, but it is not the current v2 engineering model because it depends on retired assumptions such as helical anchors, the old ballast volume, and the old gantry-centered operating sequence.

This file defines what the v2 model needs to replace or reinterpret.

## What Carries Forward

- Lunar gravity convention.
- 14 m landing pad reference geometry.
- 154 m2 pad area approximation.
- 154 one-square-meter tile reference count, if tile construction remains selected.
- Energy and battery accounting structure.
- Sensitivity-table approach.
- Clear separation between calculated values, design targets, and unproven assumptions.

## What Is Retired For v2

- Treating 110,000 kg as the current working ballast mass.
- Treating 70 m3 as the current effective regolith volume.
- Treating anchors as mission-critical or creditable stability hardware.
- Modeling 8 helical anchors and anchor-to-ballast ratios.
- Modeling gantry accuracy as a primary construction constraint.
- Using the old 3 kg/s blade-auger-conveyor intake as the current excavation baseline.
- Using the old integrated cycle of fill, anchor, gantry construction, dump, and relocate.

## Required v2 Model Modules

| Module | Purpose | First Output |
|---|---|---|
| Geometry and volume | Recalculate usable regolith volume inside the 8 m x 6 m x 4 m open-top body with raised floor and mechanism clearances. | Usable fill volume and fill-height cases |
| Mass properties | Estimate dry mass, carried regolith mass, center of mass, and mass margins. | Empty, partial-fill, and full-fill COM table |
| Stability | Evaluate no-anchor stability under slope, bucket loads, arm reach, braking, and partial fill. | Stability margins by operating case |
| Bucket loads | Estimate excavation, lift, slide, curl, dump, and tooth loads. | Actuator and structure sizing ranges |
| Arm workspace | Evaluate four side-rail arms for reach, payload, stiffness, collision zones, and cooperative docking. | Workspace and payload envelope |
| Mobility | Compare wheel, track, and modular drive options for ground pressure and relocation. | Mobility trade table |
| Power and thermal | Rebuild construction, survival, sensor, actuator, heater, and thermal rejection budgets. | Daily energy and 48 h survival scenarios |
| Pad/berm sequence | Rebuild the construction sequence around bucket and arm tooling. | Task list, duration drivers, and test needs |
| Cost and launch mass | Replace precise transport-only claims with sourced ranges. | Range-based cost exposure table |

## v2 Modeling Rule

Do not promote any old v1 numerical output into v2 unless the v2 assumptions register explicitly carries it forward. When reused, label it as a reference value, not validated v2 performance.

## Next Step

Create a new runnable model file, preferably `container_phase2_v2_model.py`, that reads baseline constants from a visible dictionary and outputs a CSV plus a short markdown summary.
