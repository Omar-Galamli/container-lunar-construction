# CONTAINER Assumptions Register v1

Date: 2026-05-14
Status: Phase 0 working register

Confidence levels:

- High: repeated in current documents or basic geometry/physics.
- Medium: plausible but needs model/test refinement.
- Low: important but weakly supported or highly uncertain.

| ID | Assumption | Baseline Value | Confidence | Evidence Source | Verification Needed |
|---|---|---:|---|---|---|
| AS-001 | Lunar gravity | 1.62 m/s2 | High | Standard lunar environment value, repeated in project docs | None beyond citation cleanup |
| AS-002 | Regolith bulk density for ballast | 1,600 kg/m3 | Medium | Latest project docs and regolith references | Simulant density range test |
| AS-003 | Ballast bin volume | 70 m3 | Medium | Current master baseline | Packaging and structural model |
| AS-004 | Working ballast mass | 110,000 kg | Medium | Current master baseline | Reconcile with 70 m3 x density and operational fill margins |
| AS-005 | Lunar ballast weight | 178 kN | High | Derived from 110,000 kg x 1.62 m/s2 | Calculation check |
| AS-006 | Conservative friction coefficient | 0.8 | Medium | Latest engineering draft | Simulant interface testing |
| AS-007 | Worst lateral load | 36 kN | Low | Latest engineering draft load envelope | Subsystem force model and test |
| AS-008 | Ballast cells | 12 | Medium | Latest engineering draft | Fill/dump control test |
| AS-009 | Regolith fill throughput | 3 kg/s | Low | Project design target | Intake prototype test |
| AS-010 | Fill duration | About 10 h | Medium | Derived from 110,000 kg / 3 kg/s | Intake model/test |
| AS-011 | Anchor count | 8 | Medium | Latest engineering draft | Stability trade study |
| AS-012 | Anchor axial rating | 80 kN each | Low | Latest engineering draft | Pull-out and lateral simulant tests |
| AS-013 | Anchor length | 1 m | Medium | Latest engineering draft | Anchor installation test |
| AS-014 | Anchor helix diameter | 0.4 m | Medium | Latest engineering draft | Anchor design trade |
| AS-015 | Gantry placement accuracy | +/-2 mm | Low | Latest engineering draft | Gantry prototype, thermal/dust test |
| AS-016 | Tile size | 1 m x 1 m x 0.3 m | Medium | Current master baseline | Tile structural model and coupon/tile test |
| AS-017 | Tile count | 154 | High | Geometry of 14 m circular pad | Geometry model |
| AS-018 | Energy per tile | 8 kWh | Low | Latest engineering draft | Sintering coupon and tile tests |
| AS-019 | Microwave peak power | 25 kW | Medium | Latest engineering draft | Sintering process model/test |
| AS-020 | Solar capacity | 20 kW nameplate | Medium | Current master baseline | Power architecture trade |
| AS-021 | Solar effective average | 14 kW in favorable periods | Low | Latest engineering draft | Site/illumination model |
| AS-022 | Battery storage | 30 kWh | Low | Current master baseline | Shadow survival model |
| AS-023 | FSP support | 40 kW | Low | Current master baseline | Programmatic feasibility and power model |
| AS-024 | Full-rate daily energy demand | 380 kWh/day | Low | Latest engineering draft | Detailed operations energy model |
| AS-025 | Build duration with FSP | Under 50 days | Low | Current master baseline | Schedule model |
| AS-026 | Solar-only duration | About 80 days | Low | Current master baseline | Schedule and power model |
| AS-027 | Sintered regolith compressive strength | 250 to 348 MPa | Medium | Project-cited sintering references | Material coupon tests |
| AS-028 | Sintered regolith tensile strength | 8 to 17 MPa | Medium | Project-cited sintering references | Material coupon tests |
| AS-029 | Berm plume reduction | Major ejecta reduction; some drafts cite 90 percent | Low | Latest engineering draft | Plume analog test |
| AS-030 | MTBF target | More than 1,000 h | Low | Latest engineering draft | Reliability model and component data |

