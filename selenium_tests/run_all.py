"""
Runs every test case script (tc*.py) in this folder one after another
and prints a summary. Start the app first with: python app.py
"""
import glob
import os
import subprocess
import sys

here = os.path.dirname(os.path.abspath(__file__))
results = []
for script in sorted(glob.glob(os.path.join(here, "tc*.py"))):
    name = os.path.basename(script)
    print(f"\n=== Running {name} ===")
    passed = subprocess.run([sys.executable, script]).returncode == 0
    results.append((name, passed))

print("\n=== Summary ===")
for name, passed in results:
    print(f"{'PASS' if passed else 'FAIL'}  {name}")
print(f"{sum(p for _, p in results)}/{len(results)} passed")
sys.exit(0 if all(p for _, p in results) else 1)
