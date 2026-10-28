"""Validate a temporary copy using disposable test credentials, never real secrets.

Install requirements-dev.txt first. No firmware is uploaded and no mower is contacted.
"""
from pathlib import Path
import base64
import secrets
import shutil
import subprocess
import sys
import tempfile


def run(config, *arguments):
    return subprocess.run(
        [sys.executable, '-m', 'esphome', *arguments, str(config)],
        capture_output=True, text=True, encoding='utf-8', errors='replace',
    )


def main():
    source = Path(__file__).with_name('automower-310.yaml')
    with tempfile.TemporaryDirectory(prefix='mower-check-') as directory:
        config = Path(directory) / source.name
        shutil.copyfile(source, config)
        missing = run(config, 'config')
        if missing.returncode == 0 or 'secrets.yaml' not in missing.stdout + missing.stderr:
            raise RuntimeError('Expected validation to fail specifically because secrets.yaml is missing')
        print('PASS: missing secrets prevent validation')
        key = base64.b64encode(secrets.token_bytes(32)).decode()
        (config.parent / 'secrets.yaml').write_text(
            'automower_pin: "0123"\n'
            'wifi_ssid: "test-network"\n'
            'wifi_password: "test-only-password"\n'
            f'api_encryption_key: "{key}"\n'
            'ota_password: "test-only-ota-password"\n', encoding='utf-8',
        )
        for arguments in [('config',), ('compile', '--only-generate')]:
            result = run(config, *arguments)
            if result.returncode:
                # Only temporary test credentials were used for this run.
                print(result.stdout + result.stderr)
                raise RuntimeError(f'ESPHome check failed: {arguments}')
            print(f'PASS: ESPHome {" ".join(arguments)}')
        generated = list(config.parent.rglob('main.cpp'))
        if not any('const std::string pin_text = "0123";' in p.read_text(encoding='utf-8') for p in generated):
            raise RuntimeError('Leading zero was not preserved in generated C++')
        print('PASS: leading zero preserved in generated PIN')
    print('No full firmware compilation or physical test was performed by this script.')


if __name__ == '__main__':
    main()
