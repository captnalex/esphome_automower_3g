"""Check static UART frames without loading secrets or contacting a mower."""
from pathlib import Path
import re


def crc8(data):
    crc = 0
    for value in data:
        for _ in range(8):
            mix = (crc ^ value) & 1
            crc >>= 1
            if mix:
                crc ^= 0x8C
            value >>= 1
    return crc


def main():
    source = Path(__file__).with_name('automower-310.yaml').read_text(encoding='utf-8')
    frames = re.findall(r'[\[{](0x02\s*,\s*0x[0-9A-Fa-f]+(?:\s*,\s*0x[0-9A-Fa-f]+)+)[\]}]', source)
    assert frames, 'No static frames found'
    for index, frame in enumerate(frames):
        values = [int(value.strip(), 16) for value in frame.split(',')]
        assert values[-1] == 3, f'Frame {index}: invalid end marker'
        assert len(values) == values[2] + 5, f'Frame {index}: invalid length'
        assert crc8(values[1:-2]) == values[-2], f'Frame {index}: invalid CRC'
    print(f'PASS: {len(frames)} static UART frames have valid length and CRC.')
    print('This does not verify protocol meaning or physical mower behavior.')


if __name__ == '__main__':
    main()
