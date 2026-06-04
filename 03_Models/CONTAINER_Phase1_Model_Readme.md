# CONTAINER Phase 1 Model Readme

Date: 2026-05-14

## Purpose

This folder contains the first analytical model for CONTAINER. The model is deliberately simple and transparent. It is meant to show which assumptions dominate the project, not to serve as a final engineering analysis.

## Model Files

- `container_phase1_model.py`: runnable Python model.
- `outputs/phase1_model_results.csv`: generated scenario table.
- `outputs/phase1_model_summary.md`: generated interpretation.

## What It Calculates

- Ballast lunar weight.
- Ballast-only friction capacity.
- Static safety factor against the baseline lateral load.
- Fill time at different regolith intake rates.
- Pad area and tile count.
- Sintering energy for the tile field.
- Daily energy balance with and without FSP.
- Rough schedule scaling.
- Battery survival time for shadow scenarios.

## Current Baseline Cases

- Baseline with FSP.
- Slow fill at 1 kg/s.
- Medium fill at 2 kg/s.
- High sintering energy at 16 kWh/tile.
- Solar-only degraded scenario.
- Larger battery scenario.
- Reduced survival load scenario.

## Important Caveats

- Schedule estimates are anchored to the project's existing 50-day with-FSP and 80-day solar-only claims, then scaled by simplified assumptions.
- The model does not yet include detailed task sequencing, thermal bottlenecks, equipment downtime, maintenance, or site traversal.
- Anchor capacity is not credited in the ballast-only friction safety factor. This is intentional so the model shows why anchors matter.
- The battery model is a simple energy-only survival check and does not yet model thermal mass, heaters cycling, or phase-change material.

## Next Improvements

- Add detailed daily task sequence.
- Add tile production rate from process time instead of using only energy.
- Add anchor contribution and degraded-anchor cases.
- Add radiator heat rejection limit.
- Add launch mass and packaging margins.
- Add cost ranges with uncertainty.

