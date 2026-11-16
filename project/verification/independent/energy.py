#!/usr/bin/env python3
"""System-level, battery-referred charge budget for the documented bring-up duty cycle."""
import csv
from dataclasses import dataclass, asdict
import json
from math import exp
from pathlib import Path

ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Profile:
    name: str
    sleep_ua: float
    cell_v: float
    efficiency: float
    boot_s: float            # includes SPI and NVM traffic, sensor elapsed time and shutdown
    platform_boot_ma: float
    platform_busy_ma: float  # MCU + miscellaneous load while waiting for the panel
    panel_ma: float
    partial_s: float
    full_s: float
    bme_uc: float            # additional sensor current integrated over a conversion
    full_count: int
    radio_events: int        # additional button-generated 2 second factory advertising windows
    radio_ma: float          # entire active platform in each radio window
    usable_fraction: float   # aggregate capacity margin for partial SOC, cold, cutoff and aging
    self_discharge_fraction_per_30d: float
    net_solar_ma: float      # conditional measured NET current into battery during usable light
    skip_count: int = 0      # wake/RTC/BME/ADC still run; no display waveform or SPI frame


PROFILES = [
    Profile('room_illustration', 12, 3.7, .87, .60, 6, 1, 5.6, .42, 3, 5, 16, 0, 8, .80, .02, 20),
    Profile('qualification_envelope', 30, 3.4, .80, .70, 10, 3, 15, 1, 6, 20, 16, 3, 15, .65, .03, 20),
    Profile('cold_full_only_charge_inhibited', 40, 3.35, .74, .9, 12, 4, 18, 1, 8, 25, 96, 3, 20, .50, .03, 0),
    Profile('below_display_floor_no_harvest', 40, 3.1, .74, .20, 8, 0, 0, 0, 0, 25, 0, 0, 0, .10, .03, 0, 96),
]


def budget(c):
    period_s, pack_mah, main_v, radio_s = 15 * 60, 250, 3.3, 2
    events = 86400 // period_s
    assert 0 <= c.full_count+c.skip_count <= events and 0 < c.efficiency <= 1
    partials = events - c.full_count-c.skip_count
    if c.cell_v<3.3:assert partials==0 and c.full_count==0 and c.radio_events==0
    waveform_s = c.full_count * c.full_s + partials * c.partial_s
    awake_s = events * c.boot_s + waveform_s + c.radio_events * radio_s
    off_s = 86400 - awake_s
    assert off_s > 0
    off_mah = c.sleep_ua * off_s / (3600 * 1000)
    main_mah = (events * c.boot_s * c.platform_boot_ma + waveform_s *
                (c.platform_busy_ma + c.panel_ma) + c.radio_events * radio_s * c.radio_ma +
                events * c.bme_uc / 1000) / 3600
    awake_bat_mah = main_mah * main_v / (c.efficiency * c.cell_v)
    # AON circuitry stays powered during refreshes. Count the same floor in those windows.
    aon_awake_mah = c.sleep_ua * awake_s / (3600 * 1000)
    electronics = off_mah + aon_awake_mah + awake_bat_mah
    self_discharge = pack_mah * c.self_discharge_fraction_per_30d / 30
    including_pack = electronics + self_discharge
    return dict(case=c.name, full_events=c.full_count, partial_events=partials, skipped_panel_events=c.skip_count,
                total_awake_s=awake_s, standby_mAh=off_mah+aon_awake_mah,
                main_input_mAh=awake_bat_mah, electronics_mAh_day=electronics,
                estimated_pack_self_discharge_mAh_day=self_discharge,
                cell_total_mAh_day=including_pack, battery_energy_mWh_day=including_pack*c.cell_v,
                illustrative_days_without_light=pack_mah*c.usable_fraction/including_pack,
                break_even_minutes_at_net_current=(60*including_pack/c.net_solar_ma if c.net_solar_ma > 0 else None))


def ntc_ohm(celsius):
    return 10000 * exp(3435 * (1 / (celsius + 273.15) - 1 / 298.15))


def main():
    result = [budget(c) for c in PROFILES]
    # 100ms rail settle, 2ms HW reset, 100ms recovery, 10ms SW reset,
    # 120ms wire time (2 x 15000 bytes at 2MHz), 100ms deep-sleep guard.
    assert min(p.boot_s for p in PROFILES if p.skip_count<96) >= .100+.002+.100+.010+.120+.100
    with (ROOT / 'energy-cases.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=result[0]); w.writeheader()
        for row in result:
            w.writerow({k: round(v, 5) if isinstance(v, float) else v for k, v in row.items()})
    metadata = dict(model='Charge/energy integration; temperature/silicon limits are separately qualified.',
                    inputs=[asdict(p) for p in PROFILES],
                    ntc_nominal_ohm={str(t): round(ntc_ohm(t), 1) for t in (0, 5, 10, 15, 25, 40, 45, 50)},
                    pack_full_energy_mWh=250*3.7,
                    flash_writes_worst_cell_per_scheduled_event=2/512,
                    theoretical_years_to_10000_writes=(10000*512)/(2*96*365.25),
                    methodology='Integrated VMAIN current; input energy = load energy / regulator efficiency. Profiles and usable capacity are assumptions. Any bench record supersedes the corresponding assumption.')
    (ROOT / 'energy-inputs.json').write_text(json.dumps(metadata, indent=2)+'\n')
    assert result[0]['electronics_mAh_day'] < result[1]['electronics_mAh_day'] < result[2]['electronics_mAh_day']
    assert result[1]['electronics_mAh_day'] < 2.5  # acceptance envelope including the board sleep floor
    for record in result:
        print(record['case'], f"electronics={record['electronics_mAh_day']:.3f} mAh/day", f"pack={record['cell_total_mAh_day']:.3f} mAh/day")


if __name__ == '__main__':
    main()
