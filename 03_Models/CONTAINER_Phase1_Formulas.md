# CONTAINER Phase 1 Model Formulas

Date: 2026-05-14

## Ballast and Stability

Ballast lunar weight:

```text
W_ballast_kN = ballast_mass_kg * lunar_gravity_m_s2 / 1000
```

Baseline:

```text
W_ballast_kN = 110,000 * 1.62 / 1000 = 178.2 kN
```

Friction capacity:

```text
F_friction_kN = W_ballast_kN * friction_coefficient
```

Design friction capacity after static safety factor:

```text
F_design_kN = F_friction_kN / static_safety_factor
```

Baseline:

```text
F_design_kN = 178.2 * 0.8 / 2 = 71.3 kN
```

Ballast-only friction safety factor against modeled lateral load:

```text
SF_friction = F_design_kN / lateral_load_kN
SF_friction = 71.3 / 36 = 1.98
```

Interpretation: ballast-only stability is close to the intended static margin, so anchors are critical to credible operations.

## Fill Time

```text
fill_time_h = ballast_mass_kg / fill_rate_kg_s / 3600
```

Baseline:

```text
fill_time_h = 110,000 / 3 / 3600 = 10.2 h
```

Sensitivity:

```text
1 kg/s = 30.6 h
2 kg/s = 15.3 h
3 kg/s = 10.2 h
```

## Pad Area and Tile Count

```text
pad_area_m2 = pi * (pad_diameter_m / 2)^2
```

Baseline:

```text
pad_area_m2 = pi * 7^2 = 153.9 m2
```

With 1 m2 tiles, this rounds to about 154 tiles.

## Sintering Energy

```text
tile_field_energy_kWh = tile_count * energy_per_tile_kWh
```

Baseline:

```text
tile_field_energy_kWh = 154 * 8 = 1,232 kWh
```

High-energy case:

```text
tile_field_energy_kWh = 154 * 16 = 2,464 kWh
```

## Daily Energy

Current simplified FSP scenario:

```text
available_with_fsp_kWh_day = fsp_kW * 24 + solar_effective_kW * 12
available_with_fsp = 40 * 24 + 14 * 12 = 1,128 kWh/day
```

Solar-only favorable-period scenario:

```text
available_solar_only_kWh_day = solar_effective_kW * 12
available_solar_only = 14 * 12 = 168 kWh/day
```

Interpretation: full-rate 380 kWh/day operations are easy with the simplified FSP case and not closed by solar-only operation.

## Battery Survival

```text
battery_survival_h = battery_kWh / survival_load_kW
```

Baseline:

```text
30 kWh / 1 kW = 30 h
```

48 h shortfall:

```text
shortfall_kWh = survival_load_kW * 48 - battery_kWh
shortfall = 1 * 48 - 30 = 18 kWh
```

Interpretation: 30 kWh is not enough for 48 h survival at a continuous 1 kW survival load.

