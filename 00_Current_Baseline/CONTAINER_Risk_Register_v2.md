# CONTAINER Risk Register v2

Date: 2026-06-11
Status: Revised risk register for open-top CONTAINER architecture

Scoring:

- Probability: 1 low, 5 high.
- Impact: 1 low, 5 mission-critical.
- Score = Probability x Impact.

| ID | Risk | Probability | Impact | Score | Mitigation / Next Action |
|---|---|---:|---:|---:|---|
| RSK-001 | Stability without anchors or stabilizers is lower than expected under bucket loads, arm reach, partial fill, slope, or braking. | 4 | 5 | 20 | Build v2 stability model; include fill states, bucket loads, arm payloads, slope, and dynamic cases; prototype at scale. |
| RSK-002 | Bucket excavation and lift loads exceed rail, mast, actuator, or body structure capacity. | 4 | 5 | 20 | Create bucket force model; size lift/curl/slide actuators; run FEA; test bucket in simulant. |
| RSK-003 | Dust disables or degrades bucket rails, vertical lift mast, arm rails, bearings, joints, sensors, radiators, or rear hatch seals. | 4 | 5 | 20 | Define dust endurance tests; add covers, seals, purge/cleaning modes, replaceable wear parts, and inspection routines. |
| RSK-004 | The four long-reach arms become too heavy, flexible, power-hungry, or difficult to control precisely. | 4 | 4 | 16 | Run kinematic/load study; limit payload envelope; prototype one arm/rail module before full system. |
| RSK-005 | Arm docking hands fail to align, latch, transfer load, or release reliably in dust and low gravity. | 3 | 4 | 12 | Build docking coupler prototype; test misalignment, dust contamination, load transfer, and emergency release. |
| RSK-006 | Underfloor battery/avionics bay overheats or cannot reject heat because shielding blocks radiators. | 4 | 5 | 20 | Build thermal model; reserve radiator fields; separate insulation from heat rejection paths; test with load banks. |
| RSK-007 | Rear service hatch is not enough for practical maintenance of batteries, avionics, PDU, cooling loops, and connectors. | 3 | 4 | 12 | Create service mockup; define slide-out trays, connector access, hatch dimensions, and tool clearances. |
| RSK-008 | Radiation/thermal shielding adds too much mass or conflicts with rails, sensors, arms, bucket travel, or radiator fields. | 3 | 4 | 12 | Develop shield panel layout; run mass/thermal trade; use removable panels around service and mechanism zones. |
| RSK-009 | Sensor count is high but coverage still has blind spots around bucket teeth, arm workspaces, rear service area, or internal fill state. | 3 | 4 | 12 | Build sensor coverage simulation; place cameras by fields of view; test dust/lighting degradation. |
| RSK-010 | Sensor/camera contamination from lunar dust causes perception failure. | 4 | 4 | 16 | Add protected windows, dust shutters, redundant views, cleaning methods, and degraded perception modes. |
| RSK-011 | Mobility module geometry is unresolved and may not support the mass, ground pressure, or relocation needs of the v2 body. | 4 | 5 | 20 | Start wheel/track trade; model ground pressure at empty, partial, and filled states; define drive-module interfaces. |
| RSK-012 | Effective regolith volume and working mass are lower than the old 70 m3 / 110,000 kg baseline after raised floor and mechanism clearances. | 4 | 4 | 16 | Recalculate internal volume; model usable fill height, slosh/shift, and center-of-mass margins. |
| RSK-013 | Pad/berm construction method no longer maps cleanly from gantry tooling to bucket/arm tooling. | 4 | 4 | 16 | Redefine construction sequence around bucket, arms, detachable tools, and external support equipment. |
| RSK-014 | Sintering energy per tile is higher than assumed, making the power system or schedule infeasible. | 4 | 5 | 20 | Keep coupon/tile energy tests; evaluate smaller demonstrator mission and alternative pad processes. |
| RSK-015 | Batteries are insufficient for 48 h shadow survival after v2 avionics, heaters, sensors, and mechanisms are added. | 4 | 4 | 16 | Build survival power model; separate survival and construction loads; resize battery/thermal buffering. |
| RSK-016 | The system is too complex for a single autonomous landed asset. | 3 | 5 | 15 | Stage development around minimum viable bucket/container/arm cycle; defer noncritical tools. |
| RSK-017 | Cost and launch mass claims become indefensible after adding arms, lift bucket, shields, batteries, avionics, and sensors. | 4 | 4 | 16 | Rebuild mass/cost model from v2 BOM; avoid precise claims until sourced. |
| RSK-018 | Public documentation remains inconsistent, with old gantry/anchor claims mixed with v2 architecture. | 3 | 4 | 12 | Maintain v2 duplicate documents; mark v1 as historical; update public summaries only after review. |
| RSK-019 | Requirements are not traceable to tests after the architecture change. | 3 | 4 | 12 | Maintain v2 requirements and verification matrix; map every new subsystem to test evidence. |
