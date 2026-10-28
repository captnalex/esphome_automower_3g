# Validation

Validated on 2026-10-28 with ESPHome 2026.10.1, using disposable test credentials only.

## Passed

- ESPHome configuration validation of the English YAML.
- ESPHome C++ source generation (`compile --only-generate`). This is not a full firmware build.
- Full ESP32-C3 / ESP-IDF 5.5.6 firmware compilation succeeded using the English configuration and disposable test credentials. RAM: 103,189 / 321,296 bytes (32.1%). Flash: 831,387 / 1,835,008 bytes (45.3%). Test firmware is not distributed.
- Missing `secrets.yaml` prevents validation.
- A leading-zero test PIN remains a four-character string in generated C++.
- All 17 static UART frames have valid lengths and Dallas CRC8 checksums. This verifies framing, not the meaning of the commands.
- The original personal PIN, API key and private subnet are absent from the distribution files.
- Git ignore rules exclude `secrets.yaml`, build folders and firmware binaries.

## Limitations

- No firmware has been installed on a device and no physical mower test has been performed for this edition.
- Original hardware observations are reported by the owner, not independently repeated here. AUX1 pin 6 is confirmed by the owner as 5 V; current capacity and sleep behavior remain unverified.
- ESPHome 2026.10.1 accepts the OTA password configuration but emits a recommendation to use OTA encryption instead to reduce flash/RAM use. API encryption remains configured separately.
- The Windows build emitted long-path warnings while configuring the bootloader, but the complete build succeeded.

## Repeat the checks

Install `requirements-dev.txt`, then run:

```sh
python check_frames.py
python check_config.py
```

`check_config.py` creates a temporary copy with disposable credentials, verifies missing-secrets failure, validates the configuration and generates C++. It does not upload firmware or contact a mower.

For a full firmware build, configure your private `secrets.yaml` locally and run `esphome compile automower-310.yaml`, or select Install in ESPHome Device Builder. Never publish the resulting firmware or generated source: they contain your secrets.
