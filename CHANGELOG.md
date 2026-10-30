# Changelog

## Wheel speed unit correction (2026-10-30)

- Correct left/right wheel speed units from rpm to mm/s, based on the owner's observation. The reported numeric value is unchanged: 394 is shown as 394 mm/s.
- Keep blade motor speed in rpm and preserve existing entity names/IDs.


## v3.10-test1 - public update (2026-10-29)

- Add guarded timer endpoint editing: select, load, edit time/weekdays, explicitly apply, and verify by readback. Editing defaults off after reboot.
- Add persistent Skip mowing today and cancellation, using HOME without changing the saved schedule. Restore AUTO next local day/next wake only when previously in AUTO. STOP cancels automatic resumption.
- Synchronize date and clock together, preserve display format and distinguish complete confirmation from partial failure.
- Add timer draft/result controls, skip status, English operation/testing instructions and migration guidance for existing Secrets.
- Include 17 compile-time C++ input-parser tests. Full firmware compilation passes with ESPHome 2026.10.1.
- Keep all credentials in Secrets in the public YAML. No rain automation or wake hardware was added.

The owner confirmed on 2026-10-29 that this version has been tested on their Husqvarna Automower 310. Other Gen3 models have not been tested.

## v3.9-test1 - included changes

- Read both timer start/end endpoints and expose days/enabled state.
- Show next start as local date/time while retaining the Unix text field.
- Distinguish control requests, acknowledgement, observed status, rejection and timeout. Avoid claiming a physical stop from a UART acknowledgement.
- Owner logs show accepted PIN, normal readings and timer responses without recorded CRC/rejection errors. Weekday/next-start interpretation and command behavior remain to be checked against the mower.

## v3.8 - shareable English edition

- Read the PIN and API encryption key from ESPHome Secrets.
- Validate four decimal PIN digits and preserve leading zeros.
- Require an OTA password from Secrets.
- Replace the original private static IP configuration with DHCP.
- Require fresh UART communication before automatic authentication.
- Translate entity labels, status messages, comments and internal identifiers into English.
- Document setup through the ESPHome app, wiring (including AUX1 pin 6: 5 V), safety and limitations.

This edition has not been physically tested on a mower.
