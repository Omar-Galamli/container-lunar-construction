# CONTAINER Phase 0 and Phase 1 Status Report v2

Date: 2026-06-15
Status: Revised status report after v2 architecture change

## Purpose

This v2 report preserves the useful Phase 0 / Phase 1 project-control work while separating it from the retired v1 gantry-and-anchor architecture. The earlier report remains available as historical context in `CONTAINER_Phase0_Phase1_Status_Report.md`.

## Completed

- Created clean project structure for baseline, evidence, models, test plans, outputs, prototype work, startup roadmap, and knowledge library.
- Created v1 baseline, requirements, assumptions, risk register, model, and digital prototype.
- Revised the technical baseline into v2 after the architecture change.
- Created v2 baseline, requirements, assumptions register, risk register, phase summary, one-page brief, and technical blueprint.
- Defined the v2 architecture around:
  - 8 m x 6 m x 4 m open-top rectangular container body.
  - Front sliding-lift toothed excavation bucket.
  - Four identical long-reach robotic arms on side rails.
  - Protected underfloor battery/avionics deck with rear service access.
  - Distributed sensor/camera manifest with 48 reference locations.
  - Body-wide radiation and thermal shield panels with functional openings.
- Retired the v1 gantry, helical anchors, stabilizer pads, outriggers, closed top, and blade-auger-conveyor intake as current architecture.

## Current v2 Findings

- The core principle remains: move light, work heavy.
- The v2 machine uses collected regolith as working mass, but the old 70 m3 / 110,000 kg ballast value must be recalculated for the open-top body, raised floor, bucket clearances, and arm workspace.
- Stability must now be proven without anchors or stabilizers. The primary cases are partial fill, full fill, bucket loading, arm reach, slope, braking, and mobility loads.
- The old Phase 1 model is still useful as a transparent v1 reference, but it should not be treated as a current v2 engineering model.
- Pad and berm construction remain the mission reference, but the construction sequence must be rebuilt around bucket and arm operations rather than gantry tooling.
- Power, battery, thermal, mobility, and cost numbers need v2 recalculation before external claims use precise values.

## Current Highest Priorities

1. Build a v2 mass, volume, and center-of-mass model.
2. Build a v2 stability model without anchors or stabilizers.
3. Estimate bucket excavation, lift, slide, and curl loads.
4. Run a side-rail arm reach, payload, stiffness, and power trade.
5. Rebuild the pad/berm construction sequence around bucket and arm tooling.
6. Rebuild power, battery, thermal, mobility, and cost ranges from v2 assumptions.
7. Mark all v1 public-facing materials as historical or superseded.

## Files To Use First

- `../00_Current_Baseline/CONTAINER_Baseline_v2.md`
- `../00_Current_Baseline/CONTAINER_Requirements_v2.md`
- `../00_Current_Baseline/CONTAINER_Assumptions_Register_v2.md`
- `../00_Current_Baseline/CONTAINER_Risk_Register_v2.md`
- `../00_Current_Baseline/CONTAINER_Phase0_Summary_v2.md`
- `CONTAINER_One_Page_Brief_v2.md`
- `CONTAINER_Technical_Blueprint_v2.md`

## Historical Files

Use these only to understand the v1 path and why the architecture changed:

- `CONTAINER_Phase0_Phase1_Status_Report.md`
- `../03_Models/CONTAINER_Phase1_Model_Readme.md`
- `../06_Digital_Prototype/README.md`
- Any document that describes the active architecture as gantry-based, anchor-stabilized, or blade-auger-conveyor fed.
