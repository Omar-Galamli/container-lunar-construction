# CONTAINER v2 Modeling Formula Notes

Date: 2026-06-15
Status: Formula transition notes for revised architecture

## Purpose

The v1 formula sheet is preserved in `CONTAINER_Phase1_Formulas.md`. This v2 sheet identifies which calculations still apply and which must be rebuilt for the open-top container, front bucket, and four side-rail robotic arms.

## Still Useful Reference Formulas

Pad area:

```text
pad_area_m2 = pi * (pad_diameter_m / 2)^2
```

For a 14 m pad:

```text
pad_area_m2 = pi * 7^2 = 153.9 m2
```

Tile-field energy, if the tile concept remains selected:

```text
tile_field_energy_kWh = tile_count * energy_per_tile_kWh
```

Battery survival:

```text
battery_survival_h = battery_kWh / survival_load_kW
```

## Retired v1 Formula Uses

The following v1 calculations should not be presented as current v2 results:

- `110,000 kg` ballast mass as a locked value.
- `70 m3` effective ballast volume as a locked value.
- Ballast-only safety factor based on the old lateral-load case as sufficient for v2.
- Anchor axial capacity and anchor-to-ballast ratios.
- Gantry accuracy formulas or assumptions as primary pad-construction constraints.

## v2 Volume and Mass Direction

The first v2 geometry model should estimate usable carried regolith volume from the open-top body:

```text
usable_volume_m3 = internal_length_m * internal_width_m * usable_fill_height_m * fill_efficiency
```

Then estimate carried regolith mass:

```text
carried_regolith_mass_kg = usable_volume_m3 * bulk_density_kg_m3
```

Mass cases should include:

- Empty vehicle.
- Low partial fill.
- Mid fill.
- Full operational fill.
- Dump/relocation state.

## v2 Stability Direction

The v2 stability model should compare resisting moment and traction margin against bucket, arm, slope, braking, and mobility loads without helical anchors:

```text
stability_margin = resisting_moment / overturning_moment
```

Required operating cases:

- Bucket full and extended.
- Bucket dumping into the container.
- One arm at maximum reach.
- Two docked arms carrying a shared load.
- Partial fill with shifted center of mass.
- Slope plus braking.
- Full fill plus relocation.

## v2 Bucket Load Direction

The bucket model should estimate:

```text
bucket_payload_kg = bucket_volume_m3 * regolith_bulk_density_kg_m3 * fill_factor
```

```text
lift_force_N = bucket_payload_kg * lunar_gravity_m_s2 + mechanism_margin_N
```

The Earth test stand may need Earth-gravity correction if simulant tests are performed on Earth.

## v2 Arm Direction

Arm calculations should estimate reach, payload, joint torque, rail carriage load, and deflection:

```text
joint_torque_Nm = payload_force_N * moment_arm_m
```

The model should report allowable payload by reach rather than a single payload number.
