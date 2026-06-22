# CONTAINER Top 10 Technical Unknowns v2

Date: 2026-06-15
Status: v2 startup risk focus list

## Purpose

These are the unknowns most likely to change the architecture, cost, schedule, or fundability of CONTAINER v2. They should guide learning, advisor questions, models, and tests.

| Rank | Unknown | Why It Matters | First Action | Evidence Needed |
|---:|---|---|---|---|
| 1 | No-anchor stability | v2 removes helical anchors, stabilizers, and outriggers, so stability must come from geometry, carried regolith, controls, and mobility limits. | Build stability model for partial fill, bucket loads, arm reach, slope, braking, and full fill. | Stability margins and scale-test data |
| 2 | Bucket excavation and lift loads | The front bucket is now the primary excavation/fill device. Loads drive actuator, rail, mast, tooth, and body design. | Build bucket force model and simple simulant test. | Excavation force, lift load, curl torque, jam, wear data |
| 3 | Usable regolith volume and mass | The old 70 m3 / 110,000 kg value may not survive raised floor, open-top geometry, mechanisms, and safe fill limits. | Recalculate internal volume and fill states. | Usable volume, fill efficiency, COM data |
| 4 | Side-rail arm reach, stiffness, and payload | Four long-reach arms may become too heavy, flexible, power-hungry, or hard to control. | Run arm kinematics/load trade and prototype one rail module. | Payload by reach, deflection, power, carriage load data |
| 5 | Arm docking/coupling reliability | Cooperative handling depends on two arms aligning, latching, transferring load, and releasing in dusty conditions. | Prototype docking hand/coupler. | Misalignment, latch, release, load-transfer, dust data |
| 6 | Dust durability | Dust can disable bucket rails, vertical lift, arm rails, bearings, seals, optics, radiators, and hatch seals. | Build dust exposure test plan. | Measured degradation, friction, jam, and contamination data |
| 7 | Power, thermal, and shadow survival | Underfloor batteries/avionics need cooling, protection, and 48 h safe-mode survival. | Build v2 power/thermal model. | Survival load, heater duty cycle, battery, radiator, thermal data |
| 8 | Mobility and ground pressure | The large body must relocate empty or partially filled without sinking, tipping, or exceeding drive loads. | Compare wheel, track, and modular drive concepts. | Ground pressure, traction, slope, sinkage, drive-load data |
| 9 | Pad/berm construction method | The old gantry tool sequence no longer applies. v2 must prove bucket/arm tooling can support useful construction. | Rebuild task sequence and define minimum useful construction analog. | Sequence, tool, flatness, compaction, placement, and inspection data |
| 10 | Cost and launch mass realism | Weak cost claims can damage startup credibility. | Build sourced dry-mass and development cost ranges. | Bottom-up mass model and comparable program data |

## Decision Rule

Any unknown ranked 1-6 can change the v2 baseline architecture. Do not lock an integrated demonstrator design until these have at least first-pass model or experiment evidence.
