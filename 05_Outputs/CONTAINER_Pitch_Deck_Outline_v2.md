# CONTAINER Pitch Deck Outline v2

Date: 2026-06-15
Status: Revised outline for v2 architecture

This is a content outline for a future 10 to 12 slide deck. It keeps the story evidence-first and avoids presenting the v2 architecture as validated hardware.

## Slide 1: CONTAINER

Open-top lunar regolith construction machine for landing pad and berm preparation.

## Slide 2: The Lunar Construction Problem

- Low gravity reduces traction, reaction force, excavation performance, and compaction force.
- Dust and plume ejecta threaten nearby assets.
- Prepared landing pads and berms are early lunar infrastructure needs.
- Launching permanently massive construction machines is expensive.

## Slide 3: Core Insight

Launch mass and working mass do not need to be the same. CONTAINER lands lighter, collects local regolith into its body, uses that material as working mass, and then places or dumps it into useful site infrastructure.

## Slide 4: Mission Baseline

- 14 m cargo landing pad reference target.
- About 1.2 m protective berm at about 5 m stand-off.
- Lunar south-polar worksite assumption.
- 45 to 50 metric ton cargo lander class.

## Slide 5: v2 System Architecture

- 8 m x 6 m x 4 m open-top rectangular container body.
- Front sliding-lift toothed excavation bucket.
- Four identical long-reach robotic arms on side rails.
- Protected underfloor battery/avionics deck with rear service access.
- Distributed sensors/cameras and shielded body panels.
- No gantry, no helical anchors, no stabilizers, no outriggers, no closed top.

## Slide 6: v2 Operating Cycle

Land, survey, excavate with bucket, fill the open container, manage center of mass, use side arms for handling/inspection/placement, build or support pad and berm operations, dump or place regolith, relocate lighter, repeat.

## Slide 7: Current Evidence

Use the v2 baseline set:

- `00_Current_Baseline/CONTAINER_Baseline_v2.md`
- `00_Current_Baseline/CONTAINER_Requirements_v2.md`
- `00_Current_Baseline/CONTAINER_Assumptions_Register_v2.md`
- `00_Current_Baseline/CONTAINER_Risk_Register_v2.md`
- `05_Outputs/CONTAINER_One_Page_Brief_v2.md`

## Slide 8: What Changed From v1

- Removed gantry and anchor dependency.
- Replaced blade-auger-conveyor intake with front bucket.
- Added four side-rail robotic arms.
- Moved batteries/avionics to an underfloor deck with rear access.
- Made v2 stability a no-anchor problem.

## Slide 9: Highest v2 Risks

- No-anchor stability under bucket, arm, slope, braking, and partial-fill cases.
- Bucket excavation/lift/curl loads.
- Arm reach, stiffness, payload, docking, and dust tolerance.
- Thermal management for underfloor power and avionics.
- Mobility and ground pressure for the large body.
- Revalidating pad/berm construction without gantry tooling.

## Slide 10: Validation Roadmap

- v2 mass, volume, and center-of-mass model.
- Bucket force and simulant excavation test.
- One side-rail arm/carriage test.
- Dust exposure test for rails, joints, sensors, and hatch seals.
- Power/thermal survival model and load-bank test.
- Subscale fill, dump, and relocation demonstrator.

## Slide 11: What We Need Next

- Technical reviewers.
- Regolith simulant and test-design support.
- Robotics and mechanism advisors.
- Power/thermal expertise.
- University or lab collaboration.
- Prototype budget for focused subsystem tests.

## Slide 12: Bottom Line

CONTAINER v2 is promising because it keeps the move-light/work-heavy insight while simplifying away the retired gantry-and-anchor architecture. The next step is measured evidence for the new bucket, arm, stability, and power assumptions.
