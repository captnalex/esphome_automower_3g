"""Compile-time tests of the actual draft-input parser extracted from the YAML.

Usage: python check_cpp_logic.py PATH_TO_CXX_COMPILER
Uses C++20 static_assert, so it also works with the ESP32 cross-compiler.
No program is run, flashed, or connected to a mower.
"""
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def main():
    source = Path(__file__).with_name('automower-310.yaml').read_text(encoding='utf-8')
    start = source.index('          if (time.size() != 5')
    end = source.index('          id(write_endpoint) = index;', start)
    parser = source[start:end]
    # Remove only UI reporting, keeping the implementation's validation and parsing.
    parser = re.sub(r'id\(schedule_result\)\.publish_state\("[^"\n]*"\);', '', parser)
    parser = parser.replace('return;', 'return -1;')
    cpp = '#include <string>\n#include <cstdint>\n'
    cpp += 'constexpr int parse(const std::string &time, const std::string &days) {\n'
    cpp += parser + '\nreturn (hour << 16) | (minute << 8) | mask;\n}\n'
    valid = [('00:00', '', 0), ('08:30','Mon,Wed,Fri', (8<<16)|(30<<8)|0x15),
             ('23:59','Sun', (23<<16)|(59<<8)|0x40), ('24:00','',24<<16),
             ('10:00','Mon,Tue,Wed,Thu,Fri,Sat,Sun',(10<<16)|0x7f)]
    invalid = [('8:00','Mon'), ('24:01','Mon'), ('25:00','Mon'), ('08:60','Mon'),
               ('aa:bb','Mon'), ('-1:00','Mon'), ('08:00','Mon,Mon'),
               ('08:00','mon'), ('08:00','Mon, Tue'), ('08:00','Mon,'),
               ('08:00',',Mon'), ('08:00','Monday')]
    for time, days, expected in valid:
        cpp += f'static_assert(parse("{time}", "{days}") == {expected});\n'
    for time, days in invalid:
        cpp += f'static_assert(parse("{time}", "{days}") == -1);\n'
    with tempfile.TemporaryDirectory(prefix='mower-cpp-check-') as directory:
        test = Path(directory) / 'parser_test.cpp'
        test.write_text(cpp, encoding='utf-8')
        subprocess.run([sys.argv[1], '-std=c++20', '-fsyntax-only', str(test)], check=True)
    print(f'PASS: {len(valid)+len(invalid)} C++ compile-time tests of the YAML input parser.')
    print('These test input validation, not UART runtime, persistence or mower behavior.')


if __name__ == '__main__':
    main()
