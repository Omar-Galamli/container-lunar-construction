# CONTAINER Technical Blueprint v2

Date: 2026-06-17

Status: manufacturer-facing concept layout using the selected v2 field-machine image as visual direction. This package communicates architecture, subsystem placement, envelope control, provisional mobility layout, interface intent, and a basic rendered concept view. It still requires detailed structural design, materials selection, thermal analysis, FEA, mobility modeling, procurement drawings, and fabrication tolerances before release to manufacture.

## 0. Selected Visual Target

- Source image: `Rendered_Images/CONTAINER_Technical_Blueprint_v2_reference.png`.
- Visual intent: front-left lunar field-machine silhouette with low forward bucket, vertical lift mast, empty open bin, four rail-mounted arms, side radiator/service panels, corner sensor pods, and visible wheeled lower drive modules.
- Engineering rule: the image guides silhouette and subsystem placement. The baseline dimensions and tables below remain the controlling source.

## 1. Coordinate System and Units

- Units: millimeters unless noted.
- Datum origin: front-left-bottom outside corner of the fixed body.
- X axis: front to rear, X0 at bucket/front face and X8000 at rear service face.
- Y axis: left to right across the 6 m front face, Y0 left side and Y6000 right side.
- Z axis: vertical up, Z0 underside/base plane and Z4000 open top rim.
- Main fixed body envelope: 8000 L x 6000 W x 4000 H.

## 2. Architecture Decisions Locked In

- The main machine is an open-top rectangular regolith container/bin. There is no roof, no lid, and the bin must remain open from above.
- The gantry system is removed completely. Do not include X-Y-Z gantry rails, overhead bridges, or gantry tool heads.
- Anchors, stabilizer pads, outriggers, and leveling legs are removed completely.
- The front excavation system is a loader/excavator-style toothed bucket, not a small scoop. It moves left-right, up-down, and curl/tilt.
- Four identical long-reach robotic arms are mounted on side rails, two on each 8 m side.
- Robotic arm tips use docking hands so any two arms can temporarily latch together for cooperative handling.
- Batteries, avionics, PDU, cooling manifolds, and power health hardware sit inside a protected underfloor equipment deck below a raised internal floor.
- Rear access is the primary maintenance path for the batteries and avionics.
- Radiation and thermal shield panels cover the fixed body everywhere except functional openings for sensors, radiators, service hatches, rails, bucket travel, and arm carriage travel.
- Wheeled drive modules are included as a provisional reference mobility layout only. Final wheel/track architecture, traction, ground pressure, suspension, and structural load paths remain open engineering items.

## 3. Primary Dimensions

| Item | Specification |
|---|---:|
| Fixed body outer envelope | 8000 x 6000 x 4000 |
| Raised internal floor height | Z900 |
| Protected equipment deck | Z0 to Z900 |
| Open regolith bay height | Z900 to Z4000, nominal 3100 |
| Nominal wall thickness allowance | 150 |
| Top rim height allowance | 200 |
| Top rim width allowance | 200 |
| External shield panel allowance | 80 nominal |
| Rear service hatch zone | X8000 face, Y600 to Y5400, Z150 to Z850 |

## 4. Front Sliding-Lift Bucket Assembly

| Feature | Specification |
|---|---|
| Bucket type | Loader/excavator-style steel bucket with side cheeks, curved inner shell, cutting edge, and replaceable teeth |
| Bucket size | 2000 W x 1100 D x 1000 H nominal |
| Teeth | 8 teeth at 250 mm pitch, 350 mm tooth projection |
| Front cross-slide rail | X approx. -150, Y300 to Y5700 |
| Bucket centerline slide travel | Y1400 to Y4600 |
| Vertical lift travel | hinge Z650 to Z3300 |
| Curl/tilt range | -35 deg scoop to +115 deg dump |
| Required sensing | bucket cameras, Y/Z encoders, hinge load pins, tilt encoder, feed/fill sensor |
| Manufacturing note | Bucket carriage must keep bucket clear of side shields and allow dumping into the open-top bin without a roof/lid obstruction |

## 5. Side-Rail Robotic Arms

| Feature | Specification |
|---|---|
| Quantity | 4 identical arms |
| Layout | 2 arms on left side rail, 2 arms on right side rail |
| Rail travel | X800 to X7200 on each 8 m side |
| Rail height | Z3150 nominal |
| Rail outboard offset | 250 mm outside each side wall |
| Home positions | A1-LF X2200 Y-250 Z3150; A2-LR X5800 Y-250 Z3150; A3-RF X2200 Y6250 Z3150; A4-RR X5800 Y6250 Z3150 |
| Arm construction | 3 main links plus wrist/tool joint |
| Link lengths | 2100 + 1900 + 1200 |
| Maximum reach | 5200 from shoulder/carriage |
| End effector | universal tool plate plus docking hand/coupler |
| Cooperative behavior | any two arms can dock tip-to-tip and handle shared tools/objects |

## 6. Protected Equipment Deck

| Zone | Placement |
|---|---|
| Raised floor | Z900, sealed structural floor between regolith bay and protected equipment bay |
| Battery trays | underfloor banks, slide-out service concept through rear access path |
| Avionics/control bay | rear underfloor zone near X6600 to X7900 |
| Power distribution | rear underfloor zone, separated from battery trays and accessible through rear hatch |
| Cooling manifolds | underfloor side/service zones with rear service points |
| Rear service hatch | shielded/dust-sealed hatch on X8000 face, Y600-Y5400, Z150-Z850 |

## 7. Provisional Wheeled Mobility Reference

| Feature | Reference treatment |
|---|---|
| Status | Provisional visual/reference layout only |
| Purpose | Communicate lower drive-module packaging inspired by the selected image |
| Shown layout | Multiple wheel modules along both long sides below the lower equipment band |
| Reserved interfaces | Lower-frame hardpoints and drive-module zones below the protected body |
| Not finalized | Wheel count, diameter, width, steering, suspension stroke, motor sizing, dust sealing, traction, ground pressure, and slope performance |

## 8. Shielding and Thermal Protection

- Fixed body surfaces use segmented radiation/thermal shield panels with an 80 mm nominal packaging allowance.
- Shield panels must be removable around service zones and should not permanently trap batteries or avionics.
- Radiator/thermal rejection fields must remain exposed to space and clear of insulation blankets.
- Sensor apertures, bucket guide rails, arm rails, arm carriages, and rear hatch edges require local dust seals and replaceable wear covers.
- Regolith carried above the raised floor may add shielding over the equipment deck when filled, but the design must not rely on fill state for basic avionics protection.

## 9. Sensor and Camera Manifest

Total sensor/camera count: 48. Fixed sensors are dimensioned from the body datum. Moving sensors are dimensioned by owning moving assembly and home datum.

| ID | Type | Nominal location | Mounting note |
|---|---|---|---|
| S01 | wide camera | X300 Y300 Z3850 | upper front-left corner |
| S02 | wide camera | X300 Y5700 Z3850 | upper front-right corner |
| S03 | wide camera | X7700 Y300 Z3850 | upper rear-left corner |
| S04 | wide camera | X7700 Y5700 Z3850 | upper rear-right corner |
| S05 | hazard camera | X200 Y350 Z650 | lower front-left hazard view |
| S06 | hazard camera | X200 Y5650 Z650 | lower front-right hazard view |
| S07 | hazard camera | X7800 Y350 Z650 | lower rear-left hazard view |
| S08 | hazard camera | X7800 Y5650 Z650 | lower rear-right hazard view |
| S09 | LiDAR | X100 Y3000 Z3600 | front high perception node |
| S10 | LiDAR | X7900 Y3000 Z3600 | rear high perception node |
| S11 | radar/depth | X4000 Y100 Z2500 | left side external perception |
| S12 | radar/depth | X4000 Y5900 Z2500 | right side external perception |
| S13 | bucket camera | moving; home X-500 Y2200 Z1500 | left bucket cheek |
| S14 | bucket camera | moving; home X-500 Y3800 Z1500 | right bucket cheek |
| S15 | bucket Y encoder | X0 Y3000 Z3350 | front cross-slide carriage datum |
| S16 | bucket Z encoder | moving; home X-150 Y3000 Z950 | vertical lift mast |
| S17 | bucket load pin | moving; home X-650 Y2200 Z1000 | left hinge pin |
| S18 | bucket load pin | moving; home X-650 Y3800 Z1000 | right hinge pin |
| S19 | bucket tilt encoder | moving; home X-650 Y3000 Z1000 | curl/tilt joint |
| S20 | feed/fill flow | X350 Y3000 Z3450 | front upper internal feed zone |
| S21 | arm wrist camera | moving on A1-LF | A1 end-effector head |
| S22 | arm force/torque | moving on A1-LF | A1 wrist load cell |
| S23 | arm rail encoder | A1 carriage home X2200 Y-250 Z3150 | left-front carriage |
| S24 | arm wrist camera | moving on A2-LR | A2 end-effector head |
| S25 | arm force/torque | moving on A2-LR | A2 wrist load cell |
| S26 | arm rail encoder | A2 carriage home X5800 Y-250 Z3150 | left-rear carriage |
| S27 | arm wrist camera | moving on A3-RF | A3 end-effector head |
| S28 | arm force/torque | moving on A3-RF | A3 wrist load cell |
| S29 | arm rail encoder | A3 carriage home X2200 Y6250 Z3150 | right-front carriage |
| S30 | arm wrist camera | moving on A4-RR | A4 end-effector head |
| S31 | arm force/torque | moving on A4-RR | A4 wrist load cell |
| S32 | arm rail encoder | A4 carriage home X5800 Y6250 Z3150 | right-rear carriage |
| S33 | fill depth | X900 Y900 Z3825 | internal upper front-left |
| S34 | fill depth | X900 Y5100 Z3825 | internal upper front-right |
| S35 | fill depth | X7100 Y900 Z3825 | internal upper rear-left |
| S36 | fill depth | X7100 Y5100 Z3825 | internal upper rear-right |
| S37 | bin camera | X4000 Y3000 Z3825 | internal overhead bin view |
| S38 | dust/visibility | X4000 Y3000 Z3400 | internal bin dust monitor |
| S39 | drive load/speed | X1000 Y300 Z450 | front-left drive interface |
| S40 | drive load/speed | X1000 Y5700 Z450 | front-right drive interface |
| S41 | drive load/speed | X7000 Y300 Z450 | rear-left drive interface |
| S42 | drive load/speed | X7000 Y5700 Z450 | rear-right drive interface |
| S43 | IMU | X4000 Y3000 Z1200 | protected equipment deck center |
| S44 | strain/vibration | X4000 Y3000 Z450 | lower structural frame |
| S45 | thermal camera | X4200 Y0 Z3250 | left radiator/shield field |
| S46 | thermal camera | X4200 Y6000 Z3250 | right radiator/shield field |
| S47 | dust accumulation | X4000 Y5800 Z3900 | upper rim/shield surface |
| S48 | power health | X7200 Y3000 Z650 | rear underfloor power bay |

## 10. Explicit Exclusions

- No gantry system.
- No anchors.
- No stabilizers, outriggers, or leveling feet.
- No closed roof, top hatch, or lid over the regolith bin.
- No buried, non-serviceable battery/avionics layout.

## 11. Drawing Sheet Index

| Sheet | Title |
|---|---|
| REF-001 | Selected visual target |
| GA-002 | Top view: body datum plan |
| GA-003 | Front elevation: bucket face |
| GA-004 | Right side elevation: arm rail, service panels, and bucket projection |
| GA-005 | Rear elevation: service face |
| MECH-006 | Bucket mechanism detail |
| MECH-007 | Side-rail robotic arm detail |
| MECH-008 | Motion and interface control table |
| INT-009 | Longitudinal cutaway: raised floor and equipment deck |
| INT-010 | Underfloor equipment plan |
| INT-011 | Manufacturing control notes |
| MOB-012 | Provisional wheeled mobility side reference |
| MOB-013 | Provisional wheeled drive-module interface plan |
| MOB-014 | Mobility status and open items |
| SENS-015 | Sensor distribution top view |
| SENS-016 | Sensor and camera placement manifest |
| REND-017 | Basic rendered concept view |

## 12. Open Engineering Items Before Fabrication Release

- Final drive/wheel/track module geometry, loads, traction, ground pressure, steering, suspension, and dust sealing.
- Detailed structural wall section, weld pattern, and alloy/material stack.
- Final radiation and thermal shield material selection.
- Battery capacity, battery chemistry, and thermal runaway isolation design.
- Avionics redundancy, harness routing, connector standard, and EMI/EMC design.
- Arm actuator sizing, bucket actuator sizing, FEA, and load-case validation.
- Dust sealing qualification for rails, lift mast, arm joints, camera windows, and rear hatch.
