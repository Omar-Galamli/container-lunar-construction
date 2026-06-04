# CONTAINER Risk-Ranked Experiment Roadmap

Date: 2026-06-01
Status: Working experiment roadmap

## Purpose

The first experiments should not try to build the whole machine. They should measure the assumptions most likely to break the startup story.

## Experiment Priority

| Priority | Experiment | Main Question | Minimum Useful Output | Updates |
|---:|---|---|---|---|
| 1 | Sintering coupon energy test | How much energy is required to create useful sintered regolith? | Energy per coupon, heating time, mass, dimensions, strength observation | AS-018, power model, tile concept |
| 2 | Regolith intake throughput test | Can a blade-auger-conveyor intake approach the 3 kg/s target or reveal a better scaled target? | kg/s, power draw, jam rate, particle behavior, fill uniformity | AS-009, AS-010, intake architecture |
| 3 | Helical anchor pull-out and lateral test | What capacity is realistic in simulant across density and depth? | Installation torque, pull-out load, lateral load, failure mode | AS-012, AS-013, AS-014 |
| 4 | Ballast fill/dump control test | Can material be distributed and emptied between cells without bad bridging or center-of-mass behavior? | Fill time, dump time, stuck material, cell balance | AS-008, AS-003, operations sequence |
| 5 | Dust durability test | Which exposed mechanisms degrade fastest under dust exposure? | Before/after force, friction, sensor quality, jams, contamination notes | RSK-002, D-series requirements |
| 6 | Small gantry accuracy test | Can a low-cost gantry hold repeatable placement under load? | Repeatability, deflection, backlash, load sensitivity | AS-015, gantry architecture |
| 7 | Battery/shadow survival model test | What survival load is realistic and what storage is needed? | Load estimate, heater duty cycle, battery size trade | AS-022, E-004 |

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
- Results must update `CONTAINER_Startup_Truth_System.md` and, when mature enough, the baseline assumptions register.

## Integrated Demonstrator Gate

Do not start the integrated demonstrator until these have first-pass results:

- Intake throughput.
- Anchor pull-out.
- Ballast fill/dump.
- Gantry accuracy.
- Sintering or construction analog.

