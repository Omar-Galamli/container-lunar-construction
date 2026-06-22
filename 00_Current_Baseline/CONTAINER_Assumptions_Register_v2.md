# CONTAINER Assumptions Register v2

Date: 2026-06-11
Status: Revised working assumptions after architecture change

Confidence levels:

- High: explicit user/design decision or basic geometry.
- Medium: plausible design target needing model/test refinement.
- Low: important but weakly supported, newly introduced, or highly uncertain.

| ID | Assumption | Baseline v2 Value | Confidence | Evidence Source | Verification Needed |
|---|---|---:|---|---|---|
| AS-001 | Lunar gravity | 1.62 m/s2 | High | Standard lunar environment value | None beyond citation cleanup |
| AS-002 | Main body outer envelope | 8 m x 6 m x 4 m | High | Locked design decision | Drawing/model check |
| AS-003 | Main body type | Open-top rectangular container/bin | High | Locked design decision | Drawing/model check |
| AS-004 | Gantry system | Removed | High | Locked design decision | Design review |
| AS-005 | Anchors/stabilizers | Removed | High | Locked design decision | Design review |
| AS-006 | Raised internal floor height | Z900 mm | Medium | v2 packaging concept | Structural and equipment packaging model |
| AS-007 | Open regolith bay height | About 3.1 m | Medium | Derived from 4 m body height and Z900 floor | Volume/structural model |
| AS-008 | Underfloor equipment bay height | About 0.9 m | Medium | v2 packaging concept | Battery/avionics/routing layout |
| AS-009 | Nominal wall allowance | 150 mm | Low | v2 drawing placeholder | Structural sizing and FEA |
| AS-010 | Nominal rim allowance | 200 mm | Low | v2 drawing placeholder | Structural sizing and FEA |
| AS-011 | Nominal shield allowance | 80 mm | Low | v2 drawing placeholder | Shield material selection and thermal analysis |
| AS-012 | Regolith bulk density for carried mass | 1,600 kg/m3 | Medium | Existing project convention | Simulant density range test |
| AS-013 | Effective regolith capacity | To be recalculated for v2 geometry | Low | Previous 70 m3 no longer directly valid | Volume model and fill constraints |
| AS-014 | Working ballast mass | To be recalculated after internal volume and fill limits | Low | Old 110,000 kg value retired pending v2 model | Stability/mass model |
| AS-015 | Stability approach | Body mass, carried regolith, geometry, controls; no anchors | Low | v2 architecture decision | Stability model and physical test |
| AS-016 | Worst lateral load | 36 kN reference retained for comparison only | Low | Existing project draft | New bucket/arm/mobility force model |
| AS-017 | Front excavation system | Toothed loader/excavator-style bucket | High | Locked design decision | Prototype test |
| AS-018 | Bucket nominal size | 2,000 W x 1,100 D x 1,000 H mm | Medium | v2 drawing reference | Excavation/load packaging study |
| AS-019 | Bucket teeth | 8 teeth, about 350 mm projection | Medium | v2 drawing reference | Cutting force and wear study |
| AS-020 | Bucket Y slide range | Y1400 to Y4600 centerline | Medium | v2 drawing reference | Rail/carriage design |
| AS-021 | Bucket Z lift range | hinge Z650 to Z3300 | Medium | v2 drawing reference | Lift actuator and structural design |
| AS-022 | Bucket curl/tilt range | -35 deg scoop to +115 deg dump | Low | v2 drawing reference | Mechanism design and interference check |
| AS-023 | Arm count | 4 identical arms | High | Locked design decision | Drawing/model check |
| AS-024 | Arm layout | Two arms per 8 m side rail | High | Locked design decision | Drawing/model check |
| AS-025 | Arm rail travel | X800 to X7200 | Medium | v2 drawing reference | Rail/carriage design |
| AS-026 | Arm reach | About 5.2 m | Medium | v2 drawing reference | Actuator sizing and workspace analysis |
| AS-027 | Arm link lengths | 2.1 m + 1.9 m + 1.2 m | Low | v2 drawing reference | Kinematic and load study |
| AS-028 | Arm docking hands | All arms have compatible couplers | High | Locked design decision | End-effector prototype |
| AS-029 | Sensor/camera minimum | At least 40; v2 manifest uses 48 | High | Locked design decision | Sensor layout and coverage analysis |
| AS-030 | Rear access | Primary service hatch on rear face | High | Locked design decision | Service demonstration |
| AS-031 | Battery storage | To be resized for v2 | Low | Old 30 kWh value retired pending power model | Shadow survival and operations model |
| AS-032 | Power architecture | Solar, battery, optional FSP scenario | Medium | Existing project direction | Power trade study |
| AS-033 | Full-rate daily energy demand | To be recalculated for v2 | Low | Old 380 kWh/day no longer directly valid | Operations energy model |
| AS-034 | Pad tile size | 1 m x 1 m x 0.3 m retained as reference only | Medium | Existing project convention | Revalidate with v2 tooling |
| AS-035 | Tile count | About 154 for 14 m pad geometry | High | Geometry of 14 m circular pad | Geometry model |
| AS-036 | Sintering energy per tile | 8 kWh reference retained pending validation | Low | Existing project draft | Coupon and tile tests |
| AS-037 | Build duration | To be recalculated for v2 | Low | Old schedule retired pending v2 model | Schedule model |
| AS-038 | Mobility configuration | Lower drive-module interface reserved; final wheel/track design TBD | Low | v2 drawing reference | Mobility trade and ground pressure model |
