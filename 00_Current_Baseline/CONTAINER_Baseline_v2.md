# CONTAINER Baseline v2

Date: 2026-06-11
Status: Revised working baseline after architecture change

## 1. Positioning

CONTAINER is an early-stage lunar infrastructure concept for a large open-top regolith construction machine. The vehicle lands as a lighter system, collects local lunar regolith into its main container body, uses the carried regolith as working mass, and performs excavation, handling, inspection, and construction tasks using a front sliding-lift bucket and four long-reach side-rail robotic arms.

This version replaces the earlier gantry-and-anchor architecture. The revised baseline is not a final fabrication release. It is a manufacturer-readable concept baseline pending detailed structural design, actuator sizing, thermal analysis, controls design, FEA, and prototype validation.

## 2. Primary Mission

The baseline mission remains construction support for a lunar cargo landing site: prepare, move, place, inspect, and manage regolith for landing pad and berm construction at a lunar south-polar worksite.

| Item | Baseline v2 |
|---|---:|
| Site type | Lunar south-polar construction site |
| Target lander class | 45 to 50 metric ton cargo lander |
| Pad usable diameter | 14 m target remains the mission reference |
| Berm stand-off from pad | About 5 m |
| Berm height | About 1.2 m |
| Main body envelope | 8 m length x 6 m width x 4 m height |
| Main body type | Open-top rectangular regolith container/bin |
| Work-zone slope assumption | About +/-1 degree, pending mobility/stability model |
| Regolith depth assumption | More than 2 m |
| Shadow survival case | Up to 48 h reduced operation/survival, pending power model |

## 3. Core Operating Cycle

1. Land and deploy at the worksite.
2. Survey surroundings using distributed cameras, LiDAR/depth sensing, and hazard sensors.
3. Excavate local regolith with the front sliding-lift bucket.
4. Move the bucket laterally, vertically, and through curl/tilt motion to scoop and dump into the open-top container.
5. Use the four side-rail robotic arms for handling, inspection, clearing, placement, and cooperative tasks inside and outside the container.
6. Use carried regolith as working mass while maintaining center-of-mass and stability limits through sensing and operations control.
7. Place, shape, compact, sinter, inspect, or support pad/berm construction operations using attached tools and robotic handling.
8. Dump or place useful regolith, relocate in a lighter state, and repeat.

The guiding principle remains: move light, work heavy.

## 4. Current Architecture

| Subsystem | Baseline v2 Description |
|---|---|
| Main structure | 8 m x 6 m x 4 m open-top rectangular container body with reinforced rim and shielded outer panels |
| Regolith container | Open bin above a raised internal floor; nominal protected equipment deck below floor |
| Front excavation | Loader/excavator-style toothed bucket on front cross-slide and vertical lift carriage |
| Bucket motion | Lateral slide across front face, vertical lift, and curl/tilt for scoop and dump |
| Robotic manipulation | 4 identical long-reach arms on side rails, two per 8 m side |
| Arm travel | Side-rail carriages travel along the 8 m length; arms work inside and outside the container |
| Arm end effectors | Universal tool plate with docking hands so two arms can latch together |
| Sensors/cameras | At least 48 distributed sensors and cameras covering navigation, bucket, arms, container fill, mobility health, thermal, dust, and power |
| Batteries/avionics | Protected underfloor equipment deck below raised internal floor, accessible from rear service hatch |
| Protection | Radiation and thermal shield panels over fixed body surfaces, with service openings for sensors, rails, bucket, arms, radiators, and rear access |
| Mobility | Lower drive-module interface reserved; final wheel/track geometry is an open engineering item |
| Power | Solar, battery, and possible fission surface power support remain architecture-level options pending v2 power sizing |
| Thermal/dust | Radiators, shield panels, heaters, dust-resistant rail covers, sealed hatches, and protected optics required |
| Autonomy | Supervised autonomy with onboard low-level control, perception, hazard detection, safe-stop, and operator oversight |

## 5. Systems Removed From v2

These are retired from the current v2 architecture unless explicitly referenced as historical context:

- Elevated X-Y-Z gantry.
- Gantry tool bridge and gantry precision placement target.
- Helical screw anchors.
- Stabilizer pads, outriggers, and leveling feet.
- Closed top, roof, or lid over the regolith container.
- Buried battery/avionics layout without rear service access.
- Old blade-auger-conveyor intake as the primary excavation architecture.

## 6. Baseline Technical Parameters

| Parameter | Baseline v2 | Notes |
|---|---:|---|
| Fixed body outer envelope | 8,000 mm x 6,000 mm x 4,000 mm | Locked v2 body dimension |
| Body length | 8,000 mm | X axis front-to-rear |
| Body width | 6,000 mm | Y axis left-to-right across front |
| Body height | 4,000 mm | Z axis vertical |
| Raised internal floor | Z900 mm | Separates regolith bay from equipment deck |
| Protected equipment deck | Z0 to Z900 mm | Batteries, avionics, PDU, cooling manifolds |
| Open regolith bay height | About 3,100 mm | Above raised floor |
| Nominal wall allowance | 150 mm | Requires detailed structural design |
| Nominal rim allowance | 200 mm | Reinforced open-top rim |
| Nominal shield allowance | 80 mm | Radiation/thermal panel packaging allowance |
| Bucket size | About 2,000 mm W x 1,100 mm D x 1,000 mm H | Loader/excavator-style bucket |
| Bucket teeth | 8 replaceable teeth, about 350 mm projection | Current concept layout |
| Bucket centerline slide | Y1400 to Y4600 | Front lateral travel |
| Bucket hinge lift | Z650 to Z3300 | Vertical lift travel |
| Bucket curl/tilt | -35 deg scoop to +115 deg dump | Needs actuator validation |
| Arm count | 4 identical arms | Two per side |
| Arm rail travel | X800 to X7200 | On each 8 m side |
| Arm rail height | Z3150 nominal | Side-mounted high rail |
| Arm reach | About 5,200 mm | Three-link concept |
| Arm link lengths | 2,100 + 1,900 + 1,200 mm | Current concept layout |
| Sensor/camera count | 48 minimum | Distributed manifest in technical blueprint |
| Rear service hatch | X8000 face, Y600-Y5400, Z150-Z850 | Protected service access |

## 7. Near-Term Development Focus

The next phase should prove or revise the highest-impact v2 assumptions:

- Stability without anchors or stabilizers under partial fill, arm reach, bucket loading, and slope cases.
- Bucket excavation force, lift force, curl force, rail loads, and jam recovery.
- Arm actuator sizing, rail carriage loads, cooperative docking behavior, and tool interface loads.
- Underfloor battery/avionics thermal management and rear serviceability.
- Radiation/thermal shield panel material stack and radiator placement.
- Dust durability of bucket rails, lift mast, arm rails, joints, camera windows, rear hatch seals, and radiators.
- Sensor fusion and coverage with at least 48 sensors/cameras.
- Mobility module geometry, ground pressure, traction, and relocation strategy.
- Whether the construction task set should remain pad/berm production or narrow to a first demonstrable regolith handling mission.
