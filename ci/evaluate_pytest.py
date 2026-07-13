#!/usr/bin/env python3
"""Evaluate a pytest JUnit report against the PPCS baseline.

The PPCS challenge ships ONE intentional failing seed test (PPCS-001):
    tests/test_rules.py::test_marginal_discount_below_threshold_fails

CI is GREEN when either:
  - only that seed test fails (the documented "6 passed, 1 failed" baseline), or
  - a team has genuinely solved PPCS-001 and all tests pass.

CI is RED when any OTHER test fails/errors (a real regression) or when no
tests were collected (the suite could not run).

Usage: python ci/evaluate_pytest.py pytest-report.xml
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET

SEED = "test_marginal_discount_below_threshold_fails"  # PPCS-001


def main() -> int:
    report = sys.argv[1] if len(sys.argv) > 1 else "pytest-report.xml"
    root = ET.parse(report).getroot()
    suites = root.iter("testsuite") if root.tag == "testsuites" else [root]

    total = 0
    seed_failed = False
    unexpected: list[str] = []
    for suite in suites:
        for case in suite.iter("testcase"):
            total += 1
            failed = any(c.tag in ("failure", "error") for c in case)
            if not failed:
                continue
            if SEED in case.get("name", ""):
                seed_failed = True
            else:
                unexpected.append(f"{case.get('classname','')}::{case.get('name','')}")

    print(f"Collected {total} tests. PPCS-001 seed failing (expected): {seed_failed}")

    if total == 0:
        print("::error::No tests were collected — suite could not run.")
        return 1
    if unexpected:
        print("::error::Unexpected test failures (regressions):")
        for u in unexpected:
            print(f"  - {u}")
        return 1

    print("Baseline OK: only the intentional PPCS-001 seed is red (or all pass).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
