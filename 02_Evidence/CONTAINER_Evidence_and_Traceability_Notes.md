# CONTAINER Evidence and Traceability Notes

Date: 2026-05-14

## Purpose

This document tracks which parts of CONTAINER are currently grounded in repeatable project documentation, which are derived by simple calculation, and which still need outside evidence or test data.

## Strongest Current Evidence

| Topic | Current State |
|---|---|
| Core concept | Strong: repeated across every project version |
| Mission focus | Strong: 14 m pad and berm appear consistently in mature documents |
| Ballast logic | Strong as a concept; medium for exact 110,000 kg sizing |
| Tile count | Strong: 14 m circular pad area is about 154 m2 |
| Lunar ballast weight | Strong: direct calculation from mass and lunar gravity |
| Need for anchors | Strong: ballast-only stability is not generous in conservative model |

## Medium-Confidence Areas

| Topic | Why Medium |
|---|---|
| 70 m3 ballast volume | Repeated, but packaging/structure model is still rough |
| 12-cell ballast bin | Good design logic, but needs fill/dump validation |
| 8-anchor layout | Plausible and repeated in latest docs, but layout trades remain open |
| 0.4 m anchor helix | More mature than older values, but needs testing |
| Gantry accuracy target | Plausible as a target, but unproven in dust/thermal conditions |
| Hybrid power architecture | Reasonable, but depends heavily on FSP availability |

## Low-Confidence / High-Impact Areas

| Topic | Why Low |
|---|---|
| 3 kg/s fill throughput | Needs blade-auger-conveyor prototype data |
| 8 kWh per tile | Needs sintering process testing and thermal model |
| 380 kWh/day energy demand | Needs detailed task-level operations model |
| 30 kWh battery shadow survival | Current simple model shows a shortfall at 1 kW survival load |
| Anchor 80 kN axial rating | Needs simulant pull-out and lateral testing |
| Berm plume reduction | Needs plume analog test or high-quality external model |
| MTBF greater than 1,000 h | Requires component-level reliability analysis |
| Cost estimates | Phase 1 transport-only exposure is about $2.92B at $200k/kg for 14,620 kg dry mass, which conflicts with older $1.5B-style program-cost language |

## Traceability Rule Going Forward

Every major claim should be tagged as one of:

- Calculated
- Project assumption
- External source
- Test result
- Design target

The current documents should avoid presenting design targets as proven performance.
