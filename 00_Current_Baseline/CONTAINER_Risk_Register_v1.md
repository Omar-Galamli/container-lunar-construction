# CONTAINER Risk Register v1

Date: 2026-05-14
Status: Phase 0 working register

Scoring:

- Probability: 1 low, 5 high.
- Impact: 1 low, 5 mission-critical.
- Score = Probability x Impact.

| ID | Risk | Probability | Impact | Score | Mitigation / Next Action |
|---|---|---:|---:|---:|---|
| RSK-001 | Sintering energy per tile is higher than baseline, making the power system or schedule infeasible. | 4 | 5 | 20 | Build energy model; test coupons; evaluate thinner/partial-depth sintering. |
| RSK-002 | Dust disables or degrades intake, conveyor, rails, bearings, sensors, radiators, or EDS surfaces. | 4 | 5 | 20 | Define dust endurance tests; simplify exposed mechanisms; add inspection/cleaning modes. |
| RSK-003 | Sintered tile joints crack, spall, or erode under plume, thermal cycling, or landing loads. | 4 | 5 | 20 | Coupon, joint, tile, and plume analog tests; evaluate repair and reinforcement. |
| RSK-004 | Anchor capacity is lower than assumed in realistic regolith conditions. | 4 | 4 | 16 | Pull-out and lateral tests across density, slope, rock inclusion, and repeated reuse. |
| RSK-005 | The system is too complex for a single autonomous landed asset. | 3 | 5 | 15 | Stage development around minimum viable construction cycle; defer stretch functions. |
| RSK-006 | Fill throughput is below 3 kg/s due to cohesion, rocks, dust, or jams. | 4 | 4 | 16 | Prototype blade-auger-conveyor intake; model 1 kg/s and 2 kg/s cases. |
| RSK-007 | Battery capacity is insufficient for 48 h shadow survival. | 4 | 4 | 16 | Build survival power model; separate survival from construction energy; evaluate added storage/thermal buffering. |
| RSK-008 | FSP availability is unrealistic for early deployment. | 3 | 5 | 15 | Maintain solar-only degraded scenario; model shared FSP and no-FSP alternatives. |
| RSK-009 | Gantry accuracy degrades due to thermal growth, dust, or structural flexibility. | 3 | 4 | 12 | Prototype gantry metrology; include thermal compensation and dust tests. |
| RSK-010 | Mobility causes site degradation, sinkage, or inability to relocate. | 3 | 4 | 12 | Model ground pressure and relocation mass; prototype mobility only after fill/dump tests. |
| RSK-011 | Cost assumptions are not defensible; the Phase 1 transport-only estimate at $200k/kg is about $2.92B for 14,620 kg dry mass, conflicting with older low program-cost claims. | 4 | 4 | 16 | Create bottom-up cost model and ranges; avoid precise claims until sourced. |
| RSK-012 | Public documentation overstates maturity and weakens technical credibility. | 3 | 4 | 12 | Use "consolidated baseline pending validation" language; separate assumed/proven values. |
| RSK-013 | Basalt reinforcement logistics are underdeveloped. | 3 | 3 | 9 | Model rod mass, handling, placement time, and alternatives. |
| RSK-014 | Thermal rejection during sintering is underestimated. | 3 | 4 | 12 | Add radiator/thermal load model and test with load banks. |
| RSK-015 | Requirements are not traceable to tests. | 2 | 4 | 8 | Maintain requirements and verification matrix from Phase 0 onward. |
