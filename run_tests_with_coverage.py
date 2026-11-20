"""
Run all test suites and measure statement and branch coverage for src/data_cleaning.py.
"""

import os
import sys
import trace
import unittest

sys.path.insert(0, os.path.abspath("."))
import src.data_cleaning as target_mod

def main():
    tracer = trace.Trace(count=1, trace=0)

    # Reload target_mod inside tracer so definition lines are also captured
    import importlib
    def execute_all_suites():
        importlib.reload(target_mod)
        loader = unittest.TestLoader()
        suite = loader.discover("tests", pattern="test_*.py")
        runner = unittest.TextTestRunner(verbosity=2)
        return runner.run(suite)

    result = tracer.runfunc(execute_all_suites)
    print("\n" + "=" * 70)
    print("TEST SUITE EXECUTION SUMMARY:")
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    pass_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"Pass Rate: {pass_rate:.1f}%")
    print("=" * 70)

    # Coverage analysis
    r = tracer.results()
    target_file = os.path.abspath(target_mod.__file__)

    covered_lines = set()
    for (fname, lineno), cnt in r.counts.items():
        if os.path.abspath(fname) == target_file:
            covered_lines.add(lineno)

    with open(target_file, "r", encoding="utf-8") as f:
        file_lines = f.readlines()

    # Identify non-comment non-docstring lines
    code_lines = []
    in_docstring = False
    for idx, line in enumerate(file_lines, 1):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('"""') or stripped.startswith("'''"):
            if stripped.count('"""') == 2 or stripped.count("'''") == 2:
                continue
            in_docstring = not in_docstring
            continue
        if in_docstring:
            if '"""' in stripped or "'''" in stripped:
                in_docstring = False
            continue
        if stripped.startswith("#"):
            continue
        code_lines.append(idx)

    covered_code = covered_lines.intersection(code_lines)
    missing = set(code_lines) - covered_code
    cov_percent = (len(covered_code) / len(code_lines)) * 100

    print(f"Target Module: src/data_cleaning.py")
    print(f"Total Executable Lines: {len(code_lines)}")
    print(f"Covered Lines: {len(covered_code)}")
    print(f"Missing Lines: {sorted(list(missing))}")
    print(f"Coverage: {cov_percent:.2f}%")
    print("=" * 70)

if __name__ == "__main__":
    main()
