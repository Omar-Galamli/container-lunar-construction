# CONTAINER Baseline v1

Date: 2026-05-14
Status: Current working baseline for Phase 0 and Phase 1

## 1. Positioning

CONTAINER is an early-stage lunar infrastructure concept for a regolith-ballasted construction cell. It lands relatively light, fills itself with local lunar regolith to create temporary working mass, anchors itself, and uses a precision gantry with interchangeable tools to construct landing pads and berms. After completing a section, it dumps ballast into useful site infrastructure, relocates in a lighter state, and repeats.

This baseline is not a final design. It is a consolidated engineering baseline pending model refinement, subscale testing, and external technical review.

## 2. Primary Mission

The baseline mission is to construct a hardened lunar cargo landing pad and protective berm at a south-polar site.

| Item | Baseline |
|---|---:|
| Site type | Lunar south polar construction site |
| Target lander class | 45 to 50 metric ton cargo lander |
| Pad usable diameter | 14 m |
| Berm stand-off from pad | About 5 m |
| Berm height | About 1.2 m |
| Berm base width | About 4 m |
| Work-zone slope assumption | About +/-1 degree |
| Regolith depth assumption | More than 2 m |
| Shadow survival case | Up to 48 h reduced operation/survival |

## 3. Core Operating Cycle

1. Land and deploy at the worksite.
2. Survey, level, deploy skirt and outriggers.
3. Excavate and collect local regolith.
4. Fill the ballast bin while managing center of mass.
5. Install and verify helical anchors.
6. Compact subgrade and construct sintered tile surface.
7. Build and compact berm using dumped ballast and local regolith.
8. Dump remaining ballast, retract or release anchors, relocate light, and repeat.

The guiding principle is: move light, work heavy.

## 4. Current Architecture

| Subsystem | Baseline Description |
|---|---|
| Structural chassis | Deployable frame integrated with ballast bin, skirt burial, outriggers, and gantry support points |
| Ballast bin | 70 m3 regolith capacity, divided into 12 ballast cells |
| Regolith intake | Low-angle blade, 0.5 m auger, enclosed conveyor, discharge spreader, vibration/percussive assistance |
| Anchoring | 8 reusable helical screw anchors with torque monitoring |
| Mobility | Four large grousered wheels; relocates primarily after ballast is dumped or reduced |
| Backup mobility | Short-range walking/feet mode remains an ambitious variant, not required for the first proof of concept |
| Gantry | Elevated X-Y-Z gantry with interchangeable tooling and +/-2 mm placement target |
| Tooling | Anchor driver, vibratory compactor, microwave sintering head, laser finishing head, inspection sensors, reinforcement placement |
| Power | Hybrid solar, battery, and fission surface power architecture |
| Thermal/dust | Radiators, heaters, electrodynamic dust shields, labyrinth seals, solid lubricants, thermal compensation |
| Autonomy | Supervised autonomy with mission planning, low-level control, SLAM, hazard detection, and safe-stop modes |

## 5. Baseline Technical Parameters

| Parameter | Baseline | Notes |
|---|---:|---|
| Ballast volume | 70 m3 | Working assumption |
| Regolith bulk density | 1,600 kg/m3 | Drives ballast mass |
| Ballast mass | 110,000 kg | Rounded from 112,000 kg; current project convention uses 110,000 kg |
| Lunar gravity | 1.62 m/s2 | Working value |
| Lunar ballast weight | 178 kN | 110,000 kg x 1.62 m/s2 |
| Conservative friction coefficient | 0.8 | Used for Phase 1 stability model |
| Design friction capacity with SF 2.0 | About 71 kN | 178 kN x 0.8 / 2 |
| Worst lateral load | About 36 kN | From latest engineering draft load envelope |
| Anchor count | 8 | Current baseline |
| Anchor length | About 1 m | Current baseline |
| Anchor helix diameter | About 0.4 m | Current baseline |
| Anchor axial rating | About 80 kN each | Needs test calibration |
| Anchor moment rating | About 25 kN*m each | Needs test calibration |
| Fill throughput | 3 kg/s | About 10 h to fill 110,000 kg |
| Gantry accuracy target | +/-2 mm | Needs thermal/dust validation |
| Tile size | 1 m x 1 m x 0.3 m | Current pad concept |
| Tile count | About 154 | Approximate count for 14 m pad |
| Flatness target | Less than 2 cm | Pad-level requirement |
| Joint step target | Less than 1 cm | Pad-level requirement |
| Pad service life target | 10 cargo landings | Requires validation |
| Microwave peak power | About 25 kW | Current concept |
| Energy per tile | About 8 kWh | High-priority assumption |
| Solar capacity | About 20 kW | Effective average lower than nameplate |
| Battery storage | About 30 kWh | May be insufficient for 48 h survival without thermal buffering |
| FSP support | About 40 kW | Critical for full-rate operations |
| Full-rate daily energy demand | About 380 kWh/day | Current mission cadence assumption |
| Nominal build duration | Under 50 days with FSP | Needs schedule model |
| Solar-only degraded duration | About 80 days | Needs schedule model |

## 6. Version Decisions

These values are retired from the current baseline unless explicitly used as historical context:

- 4 anchors instead of 8.
- 8 ballast cells instead of 12.
- Anchor helix diameter of 0.2 to 0.3 m instead of 0.4 m.
- Friction coefficient near 1.0 as the primary design assumption.
- Claims that the design is fully resolved, final, or ready for integration.

## 7. Near-Term Development Focus

The next phase should prove or revise the highest-impact assumptions:

- Sintering energy per tile and tile production cadence.
- Dust durability of rails, seals, conveyors, sensors, radiators, and EDS surfaces.
- Anchor torque, pull-out, lateral resistance, and reuse in realistic simulant.
- Fill throughput and jam recovery for the blade-auger-conveyor intake.
- Stability margins under partial fill and worst lateral loads.
- Whether 30 kWh batteries and thermal buffering can credibly survive the 48 h shadow case.

