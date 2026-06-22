# CONTAINER Requirements v2

Date: 2026-06-11
Status: Working requirements for revised open-top CONTAINER architecture

## Requirement Levels

- SHALL: required for the v2 baseline mission concept.
- SHOULD: preferred design target.
- MAY: future option or stretch capability.

## Mission Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| M-001 | CONTAINER SHALL support construction of a hardened lunar cargo landing pad with a usable diameter target of 14 m. | Analysis, demonstration |
| M-002 | CONTAINER SHALL support construction of a protective berm approximately 1.2 m high at about 5 m stand-off from the pad. | Analysis, demonstration |
| M-003 | The baseline mission SHALL target 45 to 50 metric ton cargo lander infrastructure needs. | Analysis |
| M-004 | The baseline site SHALL assume south-polar lunar terrain with about +/-1 degree local slope, more than 2 m regolith depth, and low boulder density. | Site analysis |
| M-005 | The system SHOULD complete the pad and berm mission within a schedule justified by the v2 power, mobility, bucket, and arm models. | Schedule model, demonstration |

## Structural and Stability Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| S-001 | The fixed container body SHALL have an outer envelope of 8,000 mm length x 6,000 mm width x 4,000 mm height. | Inspection |
| S-002 | The container body SHALL be open at the top with no roof, lid, or closed top hatch obstructing regolith loading. | Inspection |
| S-003 | The container SHALL include a raised internal floor at approximately Z900 mm to separate the open regolith bay from the protected equipment deck. | Inspection |
| S-004 | The underfloor equipment deck SHALL package batteries, avionics, power distribution, cooling manifolds, and service connectors. | Inspection |
| S-005 | The system SHALL maintain stability without helical anchors, stabilizer pads, outriggers, or leveling feet. | Analysis, test |
| S-006 | The control system SHALL detect center-of-mass shift and prevent bucket or arm operations outside defined stability limits. | Test, simulation |
| S-007 | Stability analysis SHALL include partial fill, full fill, bucket loading, arm reach, tool payload, slope, and dynamic braking cases. | Analysis |

## Removed-System Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| X-001 | The v2 baseline SHALL NOT include an elevated X-Y-Z gantry, gantry bridge, or gantry tool carriage. | Design review |
| X-002 | The v2 baseline SHALL NOT include helical anchors. | Design review |
| X-003 | The v2 baseline SHALL NOT include stabilizer pads, outriggers, or leveling legs. | Design review |
| X-004 | The v2 baseline SHALL NOT bury batteries or avionics where rear access, thermal management, and replacement are impossible. | Design review |

## Front Bucket Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| B-001 | The primary excavation device SHALL be a loader/excavator-style toothed bucket mounted at the front face. | Inspection |
| B-002 | The bucket SHOULD be approximately 2,000 mm wide x 1,100 mm deep x 1,000 mm high. | Inspection |
| B-003 | The bucket SHALL include replaceable excavation teeth; the v2 reference layout uses 8 teeth with about 350 mm projection. | Inspection |
| B-004 | The bucket assembly SHALL move laterally across the front face with nominal centerline travel from Y1400 to Y4600. | Inspection, test |
| B-005 | The bucket assembly SHALL move vertically with nominal hinge height travel from Z650 to Z3300. | Inspection, test |
| B-006 | The bucket SHALL include curl/tilt motion for scoop and dump, with a reference range of -35 degrees scoop to +115 degrees dump. | Inspection, test |
| B-007 | The bucket SHALL be able to dump material into the open-top container without a roof or lid obstruction. | Demonstration |
| B-008 | The bucket assembly SHALL include position, load, tilt, and camera sensing. | Inspection, test |

## Robotic Arm Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| RA-001 | CONTAINER SHALL include 4 identical long-reach robotic arms. | Inspection |
| RA-002 | Two arms SHALL mount on the left 8 m side rail and two arms SHALL mount on the right 8 m side rail. | Inspection |
| RA-003 | Each side rail SHOULD provide carriage travel from X800 to X7200. | Inspection, test |
| RA-004 | Each arm SHOULD have a maximum reach of approximately 5,200 mm from its carriage/shoulder. | Inspection, test |
| RA-005 | Each arm SHOULD use a three-link layout with reference link lengths of 2,100 mm, 1,900 mm, and 1,200 mm plus wrist/tool joint. | Inspection |
| RA-006 | Each arm SHALL be able to work both inside the open container and outside the machine envelope. | Demonstration |
| RA-007 | Each arm SHALL include a universal tool plate. | Inspection |
| RA-008 | Each arm SHALL include a docking hand/coupler so any two arms can latch together for cooperative handling. | Demonstration |
| RA-009 | Each arm SHALL include wrist camera, force/torque sensing, and rail/carriage position sensing. | Inspection, test |

## Sensors, Cameras, and Autonomy Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| C-001 | CONTAINER SHALL include at least 40 sensors plus cameras; the v2 reference manifest defines 48 total. | Inspection |
| C-002 | Sensor coverage SHALL include navigation, hazard detection, bucket monitoring, arm monitoring, fill-level sensing, dust/visibility, thermal monitoring, mobility health, and power health. | Design review |
| C-003 | The system SHALL include perception sensors at upper corners, lower hazard zones, front/rear perception nodes, bucket, arm wrists, internal bin, radiator/shield fields, and rear equipment bay. | Inspection |
| C-004 | CONTAINER SHALL use supervised autonomy rather than relying on continuous precision teleoperation. | Architecture review |
| C-005 | The system SHALL include safe-stop modes for loss of communication, power fault, sensor fault, bucket jam, arm fault, thermal fault, and mobility fault. | Simulation, test |

## Power, Thermal, and Protection Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| E-001 | Batteries and avionics SHALL be packaged in the protected underfloor equipment deck. | Inspection |
| E-002 | Batteries and avionics SHALL be accessible from the rear service hatch. | Inspection, service demonstration |
| E-003 | The system SHALL include radiation and thermal protection panels over fixed body surfaces while preserving functional openings. | Inspection |
| E-004 | Radiator/thermal rejection surfaces SHALL remain clear of insulation or shield panels that would prevent heat rejection. | Thermal analysis, inspection |
| E-005 | The system SHALL survive shadow periods up to 48 h in reduced/safe mode, pending model validation. | Thermal and power model |
| E-006 | The power architecture MAY include solar generation, battery storage, and a fission surface power support scenario. | Model |

## Dust, Environmental, and Service Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| D-001 | Critical rails, lift mechanisms, arm joints, bearings, optics, radiators, and service hatches SHALL include dust mitigation measures. | Inspection |
| D-002 | The project SHALL test dust durability of bucket rails, vertical lift mast, arm rails, sensors/cameras, radiator surfaces, and rear hatch seals. | Dust exposure test |
| D-003 | Bearings and seals SHOULD use dust-tolerant designs such as labyrinth seals, covers, solid lubricants, and replaceable wear components. | Inspection, test |
| D-004 | Rear service access SHALL support battery tray inspection/replacement, avionics access, power distribution access, cooling loop service, and dust-sealed connectors. | Service demonstration |

## Pad and Berm Requirements

| ID | Requirement | Verification Method |
|---|---|---|
| P-001 | Pad and berm construction methods SHALL be revalidated for the v2 bucket/arm architecture. | Analysis, test |
| P-002 | Pad flatness SHOULD remain within 2 cm of nominal plane. | Measurement |
| P-003 | Tile joint steps, if tile construction remains selected, SHOULD remain below 1 cm. | Measurement |
| P-004 | The berm SHOULD use dumped or placed regolith productively and be compacted in lifts where practical. | Demonstration |
