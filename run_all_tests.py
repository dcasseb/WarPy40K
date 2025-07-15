import os
import subprocess

test_dir = 'tests'
interpreter = 'warpy_interpreter.py'

# Find all .wp40k files in the tests directory
wp40k_files = [f for f in os.listdir(test_dir) if f.endswith('.wp40k')]

if not wp40k_files:
    print('No .wp40k test files found in tests/')
    exit(1)

print(f'Found {len(wp40k_files)} test files.')

for test_file in sorted(wp40k_files):
    test_path = os.path.join(test_dir, test_file)
    print(f'\n=== Running {test_file} ===')
    try:
        result = subprocess.run(['python3', interpreter, test_path], capture_output=True, text=True, timeout=30)
        print(result.stdout)
        if result.stderr:
            print('--- STDERR ---')
            print(result.stderr)
        if result.returncode == 0:
            print(f'[PASS] {test_file}')
        else:
            print(f'[FAIL] {test_file} (exit code {result.returncode})')
    except Exception as e:
        print(f'[ERROR] {test_file}: {e}') 