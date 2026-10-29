# v3.10-test1 validation

Date: 2026-10-28. Configuration: ESP32-C3 / ESPHome 2026.10.1 / ESP-IDF 5.5.6. Only disposable credentials were used for build checks.

- ESPHome configuration validation and C++ generation passed.
- Missing Secrets block validation; a quoted leading-zero test PIN survives code generation.
- All 22 static UART frames passed length and Dallas CRC8 checks.
- 17 compile-time C++ tests passed for the actual draft time/weekday parser extracted from the YAML. These cover normal times, 24:00, all-day masks, empty day lists, malformed times, invalid ranges, duplicate/unknown weekdays, spaces and extra commas. The tests remove UI reporting only; the parsing logic is taken from the deliverable.

Full firmware compilation passed. RAM: 105,493 / 321,296 bytes (32.8%); flash: 873,735 / 1,835,008 bytes (47.6%). The final source matches the compiled candidate. Source distribution was checked for the original private PIN, API key and private network address; none are included.

## Limits

No physical test of the new date writes, timer writes or persistent skip workflow has been performed here. Input tests and compilation do not test the full UART state machine, acknowledgement timing, flash persistence or mower motion. The earlier owner log confirmed PIN acceptance, normal readings, and timer responses on v3.9-test1, but did not confirm weekdays or next-start interpretation against the mower display.

## Repeat

```sh
python check_frames.py
python check_config.py
python check_cpp_logic.py /path/to/a/c++20/compiler
```

The C++ input tests use static assertions and can run with the ESP32 cross-compiler; no executable is run. `check_config.py` validates/generates with temporary test Secrets. It does not compile or flash firmware. Build your private firmware in ESPHome Device Builder and follow TESTING.md. No firmware, actual Secrets, or generated C++ is included in the source package.
