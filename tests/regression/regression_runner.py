"""
===============================================================================
Enterprise AI Gateway (EAIG)

Regression Test Runner
===============================================================================
"""

from __future__ import annotations

import subprocess
import sys
import time
from collections import defaultdict
from dataclasses import dataclass

from tests.regression.regression_suite import TESTS

import argparse

###############################################################################
# Test Result
###############################################################################
@dataclass(slots=True)
class TestResult:
    module: str
    category: str
    level: str
    passed: bool
    elapsed: float
    return_code: int

###############################################################################
# Regression Runner
###############################################################################
class RegressionRunner:
    def __init__(self, verbose: bool = True):
        self.results: list[TestResult] = []
        self.verbose = verbose
        print(f"verbose: {self.verbose}")

    ###########################################################################
    def run(self):
        start = time.perf_counter()

        print("=" * 80)
        print("Enterprise AI Gateway (EAIG)")
        print("Regression Test Suite")
        print("=" * 80)

        for test in TESTS:
            self._run_test(test)

        total = time.perf_counter() - start
        self._print_summary(total)

    ###########################################################################
    def _run_test(self, test):
        print()
        print("-" * 80)
        print(test.module)
        print("-" * 80)

        start = time.perf_counter()
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                test.module,
            ],
            capture_output = not self.verbose,
            text = True
        )

        elapsed = time.perf_counter() - start
        passed = result.returncode == 0

        self.results.append(
            TestResult(
                module=test.module,
                category=test.category,
                level=test.level,
                passed=passed,
                elapsed=elapsed,
                return_code=result.returncode,
            )
        )

        if passed:
            print(f"PASS ({elapsed:.2f}s)")
        elif not passed and not self.verbose:
            print("\nSTDOUT")
            print(result.stdout)

            print("\nSTDERR")
            print(result.stderr)
        else:
            print(f"FAIL ({elapsed:.2f}s)")

    ###########################################################################
    def _print_summary(
        self,
        total_elapsed: float,
    ):
        print()
        print("=" * 80)
        print("Regression Summary")
        print("=" * 80)

        grouped = defaultdict(list)

        for result in self.results:
            grouped[result.category].append(result)

        total_pass = 0
        total_fail = 0

        for category in sorted(grouped):
            passed = sum(
                r.passed
                for r in grouped[category]
            )

            failed = len(grouped[category]) - passed

            total_pass += passed
            total_fail += failed

            print(
                f"{category:<25}"
                f"{passed}/{len(grouped[category])} passed"
            )

        print("-" * 80)

        print(f"TOTAL PASSED : {total_pass}")
        print(f"TOTAL FAILED : {total_fail}")
        print(f"Elapsed      : {total_elapsed:.2f}s")

        print("=" * 80)


###############################################################################
# Main
###############################################################################
def main():
    # 1. Initialize the parser
    parser = argparse.ArgumentParser(description="A script with configurable output verbosity.")

    # 2. Add the --verbose and --quiet flags
    # We also add short versions (-v and -q) for convenience
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Increase output verbosity and show debug details."
    )
    
    parser.add_argument(
        "-q", "--quite", 
        action="store_true", 
        help="Suppress standard output messages."
    )

    # 3. Parse the command-line arguments
    args = parser.parse_args()
    
    # If verbose is True, provide maximum detail.
    verbose = True  # Default.

    # 4. Decide what to do based on the flags
    if args.quite:
        # If quiet is True, keep completely silent or only print critical errors
        verbose = False
    elif args.verbose:  # Not required, but just a precaution.
        # If verbose is True, provide maximum detail
        verbose = True
        
    runner = RegressionRunner(verbose=verbose)
    runner.run()

###############################################################################
if __name__ == "__main__":
    main()
