# CONTAINER Requirements v1

Date: 2026-05-14
Status: Working requirements for Phase 0 and Phase 1

## Requirement Levels

- SHALL: required for the baseline mission.
- SHOULD: preferred design target.
- MAY: future option or stretch capability.

## Mission Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| M-001 | CONTAINER SHALL construct a hardened lunar cargo landing pad with a usable diameter of 14 m. | Analysis, demonstration |
| M-002 | CONTAINER SHALL construct a protective berm approximately 1.2 m high at about 5 m stand-off from the pad. | Analysis, demonstration |
| M-003 | The baseline mission SHALL target 45 to 50 metric ton cargo landers. | Analysis |
| M-004 | The baseline site SHALL assume south-polar lunar terrain with about +/-1 degree local slope, more than 2 m regolith depth, and low boulder density. | Site analysis |
| M-005 | The system SHOULD complete the pad and berm in less than 60 days with full-rate power support. | Schedule model, demonstration |

## Structural and Stability Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| S-001 | The ballast bin SHALL hold approximately 70 m3 of regolith. | Inspection, test |
| S-002 | The ballast system SHALL target approximately 110,000 kg of regolith working mass. | Analysis, test |
| S-003 | The ballast bin SHALL be divided into 12 controllable cells for center-of-mass management. | Inspection |
| S-004 | The system SHALL maintain stability against the baseline worst lateral load of 36 kN with a static safety factor near 2.0. | Analysis, test |
| S-005 | The control system SHALL detect center-of-mass shift and prevent operations outside defined stability margins. | Test, simulation |

## Anchoring Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| A-001 | The baseline architecture SHALL use 8 helical screw anchors. | Inspection |
| A-002 | Each anchor SHOULD be about 1 m long with an approximately 0.4 m helix diameter. | Inspection |
| A-003 | Each anchor SHOULD target about 80 kN axial capacity and about 25 kN*m moment capacity. | Analysis, pull-out test |
| A-004 | Anchor installation SHALL include torque monitoring to confirm soil engagement. | Test |
| A-005 | The system SHALL define degraded modes for at least one failed or jammed anchor. | Simulation, test |

## Regolith Intake Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| R-001 | The intake SHALL use a self-feeding blade, auger, conveyor, and spreader arrangement. | Inspection |
| R-002 | The intake SHOULD target 3 kg/s regolith throughput under favorable conditions. | Simulant test |
| R-003 | The intake SHALL include jam detection and recovery logic. | Test |
| R-004 | The intake SHALL distribute regolith between ballast cells to manage center of mass. | Test |
| R-005 | Excavation SHOULD avoid creating unsafe pits or undermining the pad/berm geometry. | Operations simulation |

## Pad and Berm Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| P-001 | The pad SHOULD use 1 m x 1 m x 0.3 m sintered tiles as the current baseline. | Analysis, test |
| P-002 | The pad SHOULD contain about 154 tiles for the baseline 14 m usable diameter. | Geometry analysis |
| P-003 | Pad flatness SHALL remain within 2 cm of nominal plane. | Measurement |
| P-004 | Tile joint steps SHALL remain below 1 cm. | Measurement |
| P-005 | Pad settlement under worst landing load SHOULD remain below 2 cm. | Structural test, analysis |
| P-006 | The pad SHOULD survive 10 cargo landings with cumulative erosion below 5 mm. | Plume analog test, analysis |
| P-007 | The berm SHOULD use dumped ballast productively and be compacted in lifts where practical. | Demonstration |

## Power and Thermal Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| E-001 | The full-rate concept SHALL model about 380 kWh/day energy demand. | Model |
| E-002 | The power architecture SHALL include solar generation, battery storage, and a 40 kW-class FSP scenario. | Model |
| E-003 | The system SHOULD support a solar-only degraded scenario. | Model |
| E-004 | The system SHALL survive shadow periods up to 48 h in reduced/safe mode, pending model validation. | Thermal and power model |
| E-005 | High-power sintering SHALL be scheduled within available power and thermal rejection limits. | Model, test |

## Dust, Thermal, and Environmental Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| D-001 | Critical rails, bearings, optics, radiators, and solar surfaces SHALL include dust mitigation measures. | Inspection |
| D-002 | The project SHALL test dust durability of intake, conveyor, gantry, sensors, and radiator/EDS surfaces. | Dust exposure test |
| D-003 | Thermal expansion SHALL be included in gantry accuracy and rail alignment analysis. | Analysis, thermal test |
| D-004 | Bearings and seals SHOULD use dust-tolerant designs such as labyrinth seals and solid lubricants. | Inspection, test |

## Autonomy and Operations Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| O-001 | CONTAINER SHALL use supervised autonomy rather than relying on continuous precision teleoperation. | Architecture review |
| O-002 | The system SHALL include safe-stop modes for loss of communication, power fault, sensor fault, jam, and anchor failure. | Simulation, test |
| O-003 | The system SHOULD support high-level Earth operator oversight with low-level onboard control. | Simulation |
| O-004 | The project SHALL maintain an operating sequence model covering fill, anchor, construct, dump, relocate, and repeat. | Model |

