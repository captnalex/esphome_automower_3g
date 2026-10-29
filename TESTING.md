# Automower 310 v3.10-test1

**Tested by the owner on a Husqvarna Automower 310**, confirmed on 2026-10-29. All implementation code was generated with ChatGPT. Protocol research is credited below. Other Gen3 models have not been tested.

## Install in ESPHome Device Builder

Back up your working YAML first. Use the existing device's Edit and Install actions. Keep your working `esphome.name`, board/pins, Wi-Fi, API encryption, OTA password and any static-IP settings. The distributable uses generic `!secret` names; your existing API key may use a different Secrets name. **Do not replace a working API/OTA credential with a placeholder.** Use the ESPHome app's Secrets editor for the keys listed in `secrets.example.yaml`, including your quoted four-digit mower PIN. Do not publish private YAML or generated firmware.

All new logic runs on the ESP32. Home Assistant supplies time and exposes the controls. There is no rain sensor, weather integration or rain automation in this candidate. A later Home Assistant automation can press **Skip mowing today**, without modifying the ESP32 code.

## Date and clock synchronization

Press **Synchronize date and clock** while parked or charging, with accepted PIN and a fresh connection. The script first reads the mower date to preserve its display-format byte, writes the Home Assistant date, requests a new readback, then synchronizes and checks the clock. A rejection, timeout, mismatch or midnight rollover does not report full success. **Last control command** distinguishes full confirmation from partial success. Date/clock synchronization is manual, not automatic at boot.

## Editing a timer

When installing on another mower, compare timer times, weekdays and next-start readings with its display before changing the schedule.

1. Park the mower and wait for fresh timer readings (up to 90 seconds).
2. Turn on **Allow experimental timer changes**. It resets to off after a reboot.
3. Select **Timer endpoint to edit**, then press **Load timer for editing**.
4. Edit **Timer draft time** (`HH:MM`) and **Timer draft weekdays** (e.g. `Mon,Wed,Fri`; exact English abbreviations, commas, no spaces or duplicates). An empty weekday field means no days. `24:00` is the documented disabled-endpoint representation.
5. Press **Apply timer endpoint** and inspect **Schedule edit result** and the mower display.

Each Apply writes only the selected start OR end endpoint, then reads it back. To change a whole interval, load/edit/apply its other endpoint separately. There is no atomic two-endpoint transaction or automatic rollback. Drafts are not writes; switching the selector without loading it prevents Apply. Changes on the mower after loading invalidate the draft when fresh polling detects them.

A confirmed endpoint means the requested time/days were read back. Check the reported enabled flag separately, especially when re-enabling a formerly disabled timer. A failed confirmation may mean the write applied but its reply was lost: inspect the mower before retrying. No write is automatically retried. STOP interrupts the workflow but cannot undo a write already sent. Older firmware may not refresh the physical display immediately; the community documentation mentions updates after restart.

## Skip mowing today

Press **Skip mowing today** while the ESP32 is reachable, with valid Home Assistant time, PIN and fresh mower status. The ESP32 records the local calendar day and requests HOME. It does not change timer settings or issue START. **Skip today status** distinguishes a request from HOME observed in a fresh mower status.

- If the mower was in AUTO when skipping began, the ESP32 requests AUTO on the next local day, or when it next wakes and receives valid time/status. AUTO can cause movement according to mower behavior and its schedule.
- If the previous mode was MAN, HOME or unknown, automatic return to AUTO is not enabled.
- **Cancel skip today** ends the hold early, restoring AUTO only if it was captured as the previous mode. Cancellation can therefore cause movement.
- A press of this configuration's **Stop mower** cancels pending settings workflows and disables automatic skip commands/resumption. A subsequent explicit skip starts a new hold; otherwise inspect the mower and use the controls manually.
- HOME/AUTO requests are retried at most once per minute while their desired mode is not observed. No automatic START command is sent. State, PIN, connectivity and transaction checks still apply.
- Skip state is saved locally across restarts. This cannot wake an unpowered ESP32. The owner's AUX1 pin 6 loses 5 V in sleep; no software in this candidate changes that. If HOME prevents the mower waking on its own, you must wake it physically before it can resume.

The ESP32 blocks ordinary START/mode selections during a skip hold or pending automatic return. STOP remains available. Network commands are not an emergency stop; keep the mower's physical safety systems intact.

## Physical test order

1. Check existing readings, PIN authentication, and all four endpoint values against the mower display.
2. Synchronize date/clock while parked. Check both physical date/time and the result message.
3. Load an endpoint and first Apply its unchanged values. Confirm the readback and display before testing a changed time/day. Save your original schedule before editing.
4. Test Skip while parked in AUTO, confirm HOME, then Cancel and confirm AUTO with the area clear. Test STOP during a skip to verify automatic resumption is cancelled.
5. Verify skip persistence/recovery and next-day behavior before depending on it unattended.

## Sources

- [Robomower V0.8 by David Gross and contributors](https://www.mikrocontroller.net/attachment/278555/Robomower_V0.8.pdf), date/time pp. 7-9, timer reads/writes pp. 22-31.
- [Wall-E community implementation](https://gitlab.com/nbrgmn/wall-e-esp8266-automower/-/blob/develop/Wall-E_ESP8266_automower.ino), corroborating timer request layouts.

These are community reverse-engineering sources, not an official Husqvarna specification. Unknown firmware variants need verification before writes. No security-level, boundary-loop or direct motor-test commands were added.
