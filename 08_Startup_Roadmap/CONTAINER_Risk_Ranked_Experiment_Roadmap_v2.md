# CONTAINER Risk-Ranked Experiment Roadmap v2

Date: 2026-06-15
Status: v2 working experiment roadmap

## Purpose

The first v2 experiments should not try to build the whole machine. They should measure the assumptions most likely to break the revised open-top container, front bucket, and side-rail arm architecture.

## Experiment Priority

| Priority | Experiment | Main Question | Minimum Useful Output | Updates |
|---:|---|---|---|---|
| 1 | v2 stability model and tabletop stability test | Can the no-anchor architecture stay within stability limits under partial fill, bucket loads, arm reach, slope, and braking? | Stability margin table, failure cases, scale-test observations | AS-015, RSK-001 |
| 2 | Bucket excavation/lift/dump test | What bucket loads, jams, and fill behavior appear in simulant? | Excavation force, payload, lift force, curl torque, dump behavior, jam notes | AS-017 to AS-022, RSK-002 |
| 3 | Open-container fill/dump and COM test | Can material be distributed and emptied without bad bridging or center-of-mass behavior? | Fill efficiency, dump time, stuck material, COM shift estimate | AS-013 to AS-015, RSK-012 |
| 4 | Side-rail arm/carriage prototype | Can a simplified side-rail arm achieve useful reach, payload, and stiffness? | Reach/payload table, deflection, power, carriage load | AS-023 to AS-027, RSK-004 |
| 5 | Arm docking/coupler test | Can two arms latch, carry, release, and recover from misalignment? | Alignment tolerance, latch/release reliability, load-transfer data | AS-028, RSK-005 |
| 6 | Dust durability test | Which exposed mechanisms degrade fastest under dust exposure? | Before/after force, friction, sensor quality, jams, contamination notes | RSK-003, RSK-010, D-series requirements |
| 7 | Battery/thermal survival model and load-bank test | What survival load is realistic and what storage/thermal rejection is needed? | Load estimate, heater duty cycle, radiator/battery trade | AS-031 to AS-033, RSK-006, RSK-015 |
| 8 | Sintering coupon or pad-surface analog test | Does the selected pad-surface method remain credible for v2 tooling? | Energy, heat time, strength observation, surface quality | AS-034 to AS-036, RSK-014 |

## Test Report Template

Each test report should include:

- Purpose and linked assumption IDs.
- Setup photos.
- Materials and dimensions.
- Procedure.
- Raw measurements.
- Observed failures.
- Result summary.
- Model or assumption update.
- Next design decision.

## Acceptance Criteria

- Every test must produce measured values.
- Videos and photos support, but do not replace, measurements.
- Failed tests are valuable if they identify a design limit.
- Results must update `CONTAINER_Startup_Truth_System_v2.md` and, when mature enough, `../00_Current_Baseline/CONTAINER_Assumptions_Register_v2.md`.

## Integrated Demonstrator Gate

Do not start the integrated v2 demonstrator until these have first-pass results:

- No-anchor stability.
- Bucket excavation/lift/dump.
- Open-container fill/dump and COM behavior.
- Side-rail arm reach/payload/stiffness.
- Dust durability.
- Battery/thermal survival model.
