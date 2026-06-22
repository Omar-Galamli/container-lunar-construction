# CONTAINER Startup Truth System v2

Date: 2026-06-15
Status: v2 evidence-control document

## Purpose

This document prevents the startup story from getting ahead of the evidence after the v2 architecture change. It connects the current concept, assumptions, models, tests, and public claims.

## Evidence Tags

Use one tag for every important claim:

| Tag | Meaning |
|---|---|
| Calculated | Direct result from geometry, physics, or a transparent model |
| Project assumption | Current baseline value that has not been independently proven |
| External source | Supported by outside literature, data, or expert input |
| Test result | Measured by a CONTAINER experiment |
| Design target | Desired performance, not yet proven |
| Retired | Older claim that should not be reused as current v2 truth |

## Current Proof Versus Assumption Table

| Claim | Current Tag | Confidence | Startup-Safe Wording | Next Verification |
|---|---|---|---|---|
| CONTAINER uses regolith as carried working mass and later infrastructure material | Project assumption | Medium | Core architecture hypothesis | Advisor review and subscale fill/dump demo |
| v2 main body is 8 m x 6 m x 4 m and open at the top | Project assumption | High | Current v2 body envelope and architecture decision | Drawing/model check |
| v2 removes gantry, helical anchors, stabilizers, outriggers, and closed top | Project assumption | High | Retired v1 systems are not part of the current baseline | Design review |
| 14 m usable landing pad requires about 154 m2 of surface | Calculated | High | Baseline pad geometry produces about 154 m2 area | Geometry check |
| 154 tiles for 1 m x 1 m tile concept | Calculated | High | Reference tile concept maps to about 154 tiles | Revalidate with v2 construction method |
| Front bucket is the primary excavation/fill device | Project assumption | Medium | v2 replaces old intake with a front sliding-lift toothed bucket | Bucket force model and simulant test |
| Four side-rail arms support handling, inspection, placement, and cooperative tasks | Project assumption | Medium | v2 uses four identical long-reach arms, pending load and control validation | Arm rail module prototype |
| No-anchor stability is sufficient | Design target | Low | v2 stability must be proven by model and test | Stability model and scale test |
| Usable carried regolith mass | Project assumption | Low | Old 110,000 kg value is retired pending v2 volume and fill model | Volume, mass, and COM model |
| 8 kWh per tile sintering energy | Project assumption | Low | High-impact energy assumption pending coupon testing | Sintering coupon or alternative pad-surface test |
| 40 kW FSP enables full-rate operations | Project assumption | Low | Full-rate case depends on FSP-class support or equivalent power | Programmatic and power trade review |
| CONTAINER is cheaper than alternatives | Retired | Low | Cost advantage is not yet established | Bottom-up cost model |
| CONTAINER is a final design | Retired | Low | Revised baseline pending validation | Keep public wording controlled |

## Startup-Safe Language

Use:

- "CONTAINER v2 is a revised baseline pending validation."
- "The current model needs to test..."
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
- "Anchors are mission-critical" when describing v2.
- "Precision gantry" when describing v2.

## Monthly Truth Review

At the end of each month:

- Promote claims only when evidence improves.
- Downgrade claims when tests or models reveal weakness.
- Move outdated wording to retired.
- Update `../00_Current_Baseline/CONTAINER_Assumptions_Register_v2.md` if the source of truth changes.
