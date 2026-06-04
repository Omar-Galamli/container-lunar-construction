#!/usr/bin/env python3
"""First-order analytical model for the CONTAINER Phase 1 baseline.

The model is intentionally simple and transparent. It is not a detailed design
tool; it is a way to expose which assumptions dominate mission feasibility.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass, asdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "03_Models" / "outputs"


@dataclass(frozen=True)
class Scenario:
    name: str
    fill_rate_kg_s: float = 3.0
    energy_per_tile_kwh: float = 8.0
    solar_effective_kw: float = 14.0
    fsp_kw: float = 40.0
    construction_energy_kwh_day: float = 380.0
    battery_kwh: float = 30.0
    survival_load_kw: float = 1.0
    daily_work_hours: float = 24.0
    schedule_efficiency: float = 0.75


@dataclass
class Results:
    scenario: str
    ballast_mass_kg: float
    ballast_weight_kn: float
    friction_capacity_kn: float
    design_friction_capacity_kn: float
    lateral_load_kn: float
    friction_safety_factor: float
    fill_time_h: float
    pad_area_m2: float
    tile_count: int
    tile_sintering_energy_kwh: float
    available_energy_with_fsp_kwh_day: float
    available_energy_solar_only_kwh_day: float
    full_rate_energy_balance_kwh_day: float
    solar_only_energy_balance_kwh_day: float
    estimated_days_with_fsp: float
    estimated_days_solar_only: float
    battery_survival_hours_at_load: float
    battery_shortfall_for_48h_kwh: float
    total_anchor_axial_capacity_kn: float
    anchor_to_ballast_weight_ratio: float
    dry_mass_kg: float
    estimated_transport_cost_usd_billion: float


BASELINE = {
    "pad_diameter_m": 14.0,
    "tile_area_m2": 1.0,
    "tile_count_override": 154,
    "ballast_mass_kg": 110_000.0,
    "lunar_gravity_m_s2": 1.62,
    "friction_coefficient": 0.8,
    "static_safety_factor": 2.0,
    "lateral_load_kn": 36.0,
    "anchor_count": 8,
    "anchor_axial_capacity_kn": 80.0,
    "dry_mass_kg": 14_620.0,
    "transport_cost_usd_per_kg": 200_000.0,
}


SCENARIOS = [
    Scenario(name="baseline_with_fsp"),
    Scenario(name="slow_fill_1kg_s", fill_rate_kg_s=1.0),
    Scenario(name="medium_fill_2kg_s", fill_rate_kg_s=2.0),
    Scenario(name="high_sinter_energy_16kwh_tile", energy_per_tile_kwh=16.0, construction_energy_kwh_day=380.0 + (154 * 8.0 / 50.0)),
    Scenario(name="solar_only_baseline", fsp_kw=0.0, construction_energy_kwh_day=250.0, daily_work_hours=12.0, schedule_efficiency=0.6),
    Scenario(name="larger_battery_100kwh", battery_kwh=100.0),
    Scenario(name="reduced_survival_load_0p3kw", survival_load_kw=0.3),
]


def compute(scenario: Scenario) -> Results:
    pad_area_m2 = math.pi * (BASELINE["pad_diameter_m"] / 2.0) ** 2
    tile_count = BASELINE["tile_count_override"] or math.ceil(pad_area_m2 / BASELINE["tile_area_m2"])

    ballast_weight_kn = (
        BASELINE["ballast_mass_kg"] * BASELINE["lunar_gravity_m_s2"] / 1000.0
    )
    friction_capacity_kn = ballast_weight_kn * BASELINE["friction_coefficient"]
    design_friction_capacity_kn = friction_capacity_kn / BASELINE["static_safety_factor"]
    lateral_load_kn = BASELINE["lateral_load_kn"]
    friction_safety_factor = design_friction_capacity_kn / lateral_load_kn

    fill_time_h = BASELINE["ballast_mass_kg"] / scenario.fill_rate_kg_s / 3600.0
    tile_sintering_energy_kwh = tile_count * scenario.energy_per_tile_kwh

    # FSP is assumed available 24 h/day. Solar effective power is treated as a
    # favorable-period average, not a 24 h guaranteed value.
    available_energy_with_fsp_kwh_day = (
        scenario.fsp_kw * 24.0 + scenario.solar_effective_kw * 12.0
    )
    available_energy_solar_only_kwh_day = scenario.solar_effective_kw * 12.0
    full_rate_energy_balance_kwh_day = (
        available_energy_with_fsp_kwh_day - scenario.construction_energy_kwh_day
    )
    solar_only_energy_balance_kwh_day = (
        available_energy_solar_only_kwh_day - scenario.construction_energy_kwh_day
    )

    # The existing baseline says about 50 days with FSP at 380 kWh/day. Use that
    # as the anchored reference, then scale by energy demand, work hours, and
    # efficiency. This keeps the model transparent while we lack task-level data.
    estimated_days_with_fsp = (
        50.0
        * (scenario.construction_energy_kwh_day / 380.0)
        * (24.0 / scenario.daily_work_hours)
        * (0.75 / scenario.schedule_efficiency)
    )
    if scenario.fsp_kw <= 0:
        estimated_days_with_fsp = float("nan")

    # Existing baseline says solar-only degraded operations are about 80 days.
    # Scale around that reference using energy and schedule efficiency.
    estimated_days_solar_only = (
        80.0
        * max(1.0, scenario.construction_energy_kwh_day / 250.0)
        * (0.6 / scenario.schedule_efficiency)
    )

    battery_survival_hours_at_load = scenario.battery_kwh / scenario.survival_load_kw
    battery_shortfall_for_48h_kwh = max(
        0.0, scenario.survival_load_kw * 48.0 - scenario.battery_kwh
    )
    total_anchor_axial_capacity_kn = (
        BASELINE["anchor_count"] * BASELINE["anchor_axial_capacity_kn"]
    )
    anchor_to_ballast_weight_ratio = total_anchor_axial_capacity_kn / ballast_weight_kn
    estimated_transport_cost_usd_billion = (
        BASELINE["dry_mass_kg"] * BASELINE["transport_cost_usd_per_kg"] / 1_000_000_000
    )

    return Results(
        scenario=scenario.name,
        ballast_mass_kg=BASELINE["ballast_mass_kg"],
        ballast_weight_kn=ballast_weight_kn,
        friction_capacity_kn=friction_capacity_kn,
        design_friction_capacity_kn=design_friction_capacity_kn,
        lateral_load_kn=lateral_load_kn,
        friction_safety_factor=friction_safety_factor,
        fill_time_h=fill_time_h,
        pad_area_m2=pad_area_m2,
        tile_count=tile_count,
        tile_sintering_energy_kwh=tile_sintering_energy_kwh,
        available_energy_with_fsp_kwh_day=available_energy_with_fsp_kwh_day,
        available_energy_solar_only_kwh_day=available_energy_solar_only_kwh_day,
        full_rate_energy_balance_kwh_day=full_rate_energy_balance_kwh_day,
        solar_only_energy_balance_kwh_day=solar_only_energy_balance_kwh_day,
        estimated_days_with_fsp=estimated_days_with_fsp,
        estimated_days_solar_only=estimated_days_solar_only,
        battery_survival_hours_at_load=battery_survival_hours_at_load,
        battery_shortfall_for_48h_kwh=battery_shortfall_for_48h_kwh,
        total_anchor_axial_capacity_kn=total_anchor_axial_capacity_kn,
        anchor_to_ballast_weight_ratio=anchor_to_ballast_weight_ratio,
        dry_mass_kg=BASELINE["dry_mass_kg"],
        estimated_transport_cost_usd_billion=estimated_transport_cost_usd_billion,
    )


def write_csv(results: list[Results]) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "phase1_model_results.csv"
    fieldnames = list(asdict(results[0]).keys())
    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(asdict(row))
    return out_path


def write_summary(results: list[Results]) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    baseline = next(r for r in results if r.scenario == "baseline_with_fsp")
    out_path = OUTPUT_DIR / "phase1_model_summary.md"
    lines = [
        "# CONTAINER Phase 1 Model Summary",
        "",
        "Generated by `container_phase1_model.py`.",
        "",
        "## Baseline Results",
        "",
        f"- Ballast lunar weight: {baseline.ballast_weight_kn:.1f} kN.",
        f"- Conservative design friction capacity: {baseline.design_friction_capacity_kn:.1f} kN.",
        f"- Baseline lateral load: {baseline.lateral_load_kn:.1f} kN.",
        f"- Ballast-only friction safety factor after static SF: {baseline.friction_safety_factor:.2f}.",
        f"- Fill time at 3 kg/s: {baseline.fill_time_h:.1f} h.",
        f"- Pad area: {baseline.pad_area_m2:.1f} m2; modeled tile count: {baseline.tile_count}.",
        f"- Sintering energy for all tiles at 8 kWh/tile: {baseline.tile_sintering_energy_kwh:.0f} kWh.",
        f"- Available daily energy with 40 kW FSP plus solar assumption: {baseline.available_energy_with_fsp_kwh_day:.0f} kWh/day.",
        f"- Full-rate daily energy balance: {baseline.full_rate_energy_balance_kwh_day:.0f} kWh/day.",
        f"- Solar-only daily energy balance against 380 kWh/day: {baseline.solar_only_energy_balance_kwh_day:.0f} kWh/day.",
        f"- 30 kWh battery survival at 1 kW load: {baseline.battery_survival_hours_at_load:.1f} h.",
        f"- Battery shortfall for 48 h at 1 kW load: {baseline.battery_shortfall_for_48h_kwh:.1f} kWh.",
        f"- Total nominal anchor axial capacity: {baseline.total_anchor_axial_capacity_kn:.0f} kN.",
        f"- Anchor axial capacity to ballast lunar weight ratio: {baseline.anchor_to_ballast_weight_ratio:.1f}x.",
        f"- Dry mass used for launch/transport costing: {baseline.dry_mass_kg:.0f} kg.",
        f"- Transport-only cost at $200k/kg: ${baseline.estimated_transport_cost_usd_billion:.2f}B.",
        "",
        "## Immediate Interpretation",
        "",
        "- Ballast-only stability is close but not generous: the model gives about 1.98 against the 36 kN lateral load after applying the static safety factor. Anchors are therefore not optional for credible operations.",
        "- Fill throughput strongly affects setup time: 3 kg/s is about 10.2 h, 2 kg/s is about 15.3 h, and 1 kg/s is about 30.6 h.",
        "- FSP makes the energy budget comfortable in this simple model; solar-only operation does not support the same daily energy demand.",
        "- The 30 kWh battery is not enough for a 48 h shadow survival case at 1 kW survival load. It only closes if survival load is reduced strongly or additional thermal storage/power is added.",
        "- Sintering energy per tile is a dominant uncertainty and should be one of the first physical tests.",
        "",
        "## Scenario Table",
        "",
        "| Scenario | Fill time h | FSP days | Solar-only days | Battery survival h | 48h battery shortfall kWh |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for result in results:
        fsp_days = "n/a" if math.isnan(result.estimated_days_with_fsp) else f"{result.estimated_days_with_fsp:.1f}"
        lines.append(
            f"| {result.scenario} | {result.fill_time_h:.1f} | {fsp_days} | "
            f"{result.estimated_days_solar_only:.1f} | {result.battery_survival_hours_at_load:.1f} | "
            f"{result.battery_shortfall_for_48h_kwh:.1f} |"
        )
    out_path.write_text("\n".join(lines) + "\n")
    return out_path


def main() -> None:
    results = [compute(scenario) for scenario in SCENARIOS]
    csv_path = write_csv(results)
    summary_path = write_summary(results)
    print(f"Wrote {csv_path}")
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()
