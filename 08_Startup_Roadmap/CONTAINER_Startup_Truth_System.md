# CONTAINER Startup Truth System

Date: 2026-06-01
Status: Working evidence-control document

## Purpose

This document prevents the startup story from getting ahead of the evidence. It connects the current concept, assumptions, models, tests, and public claims.

## Evidence Tags

Use one tag for every important claim:

| Tag | Meaning |
|---|---|
| Calculated | Direct result from geometry, physics, or a transparent model |
| Project assumption | Current baseline value that has not been independently proven |
| External source | Supported by outside literature, data, or expert input |
| Test result | Measured by a CONTAINER experiment |
| Design target | Desired performance, not yet proven |
| Retired | Older claim that should not be reused |

## Current Proof Versus Assumption Table

| Claim | Current Tag | Confidence | Startup-Safe Wording | Next Verification |
|---|---|---|---|---|
| CONTAINER uses regolith as temporary ballast and later infrastructure material | Project assumption | Medium | Core architecture hypothesis | Advisor review and subscale fill/dump demo |
| 14 m usable landing pad requires about 154 square meters of surface | Calculated | High | Baseline pad geometry produces about 154 m2 area | Geometry check |
| 154 tiles for 1 m x 1 m tile concept | Calculated | High | Current tile concept maps to about 154 tiles | CAD/model check |
| 110,000 kg ballast creates about 178 kN lunar weight | Calculated | High | Baseline ballast mass produces about 178 kN lunar weight | Calculation check |
| Ballast-only stability is close to the 36 kN lateral load case | Calculated | Medium | Ballast helps, but anchors remain mission-critical | Improve force model |
| 3 kg/s intake throughput | Design target | Low | Intake target pending simulant test | Intake prototype test |
| 8 anchors at about 80 kN axial capacity each | Design target | Low | Anchor sizing target pending simulant pull-out testing | Anchor pull-out and lateral test |
| +/-2 mm gantry accuracy | Design target | Low | Precision target pending gantry prototype and thermal/dust validation | Gantry prototype test |
| 8 kWh per tile sintering energy | Project assumption | Low | High-impact energy assumption pending coupon testing | Sintering coupon test |
| 30 kWh battery survives 48 h shadow | Retired as sufficient | Low | Current simple model shows 30 kWh is not enough at 1 kW for 48 h | Survival load and battery trade model |
| 40 kW FSP enables full-rate operations | Project assumption | Low | Full-rate case depends on FSP-class support or equivalent power | Programmatic and power trade review |
| CONTAINER is cheaper than alternatives | Retired | Low | Cost advantage is not yet established | Bottom-up cost model |
| CONTAINER is a final design | Retired | Low | Consolidated baseline pending validation | Keep public wording controlled |

## Startup-Safe Language

Use:

- "CONTAINER is a consolidated baseline pending validation."
- "The current model suggests..."
- "The baseline target is..."
- "This is a high-impact assumption."
- "The next test is designed to measure..."

Avoid:

- "Fully proven."
- "Final design."
- "Guaranteed."
- "Solves lunar construction."
- "Cheaper than all alternatives."
- "Ready for deployment."

## Monthly Truth Review

At the end of each month:

- Promote claims only when evidence improves.
- Downgrade claims when tests or models reveal weakness.
- Move outdated wording to retired.
- Update the assumptions register in `../00_Current_Baseline/CONTAINER_Assumptions_Register.md` if the source of truth changes.

