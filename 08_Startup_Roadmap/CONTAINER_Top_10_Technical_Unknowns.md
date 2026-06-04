# CONTAINER Top 10 Technical Unknowns

Date: 2026-06-01
Status: Startup risk focus list

## Purpose

These are the unknowns most likely to change the architecture, cost, schedule, or fundability of CONTAINER. They should guide learning, advisor questions, models, and tests.

| Rank | Unknown | Why It Matters | First Action | Evidence Needed |
|---:|---|---|---|---|
| 1 | Sintering energy per tile | Drives power architecture, schedule, thermal rejection, and FSP dependency | Run coupon-level literature review and simple energy model | Coupon or tile energy measurement |
| 2 | Sintered tile and joint durability | Pad must survive landing loads, thermal cycling, cracks, and plume erosion | Define coupon and joint test plan | Strength, crack, erosion, and joint data |
| 3 | Dust durability | Dust can disable intake, rails, bearings, seals, optics, radiators, and sensors | Build dust exposure test plan | Measured degradation and jam data |
| 4 | Regolith intake throughput | 3 kg/s target controls fill time and operational cadence | Prototype blade-auger-conveyor intake | Throughput, power, jam, and wear data |
| 5 | Anchor capacity in realistic regolith | Anchors are mission-critical for stability and load transfer | Design pull-out and lateral simulant test | Torque, pull-out, lateral, reuse, and failure data |
| 6 | Shadow survival and battery sizing | Current 30 kWh battery misses 48 h at 1 kW survival load | Improve survival load model | Survival load, heater, thermal storage, and battery trade data |
| 7 | FSP availability and alternatives | Full-rate operations depend on high-power support | Build FSP, solar-only, shared-power, and reduced-rate scenarios | Programmatic feasibility and power trade data |
| 8 | Gantry accuracy under dust/thermal/load | Pad quality depends on controlled placement and finishing | Build small gantry accuracy test | Repeatability, deflection, backlash, and thermal drift data |
| 9 | Cost realism | Weak cost claims can damage startup credibility | Build sourced transport and development cost ranges | Bottom-up cost model and comparable program data |
| 10 | Autonomy complexity | Single landed asset may be too complex for early deployment | Define minimum viable construction cycle | Fault modes, supervision model, and operations simulation |

## Decision Rule

Any unknown ranked 1-6 can change the baseline architecture. Do not lock the integrated demonstrator design until these have at least first-pass model or experiment evidence.

