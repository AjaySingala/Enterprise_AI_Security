"""
Run:
python -m tests.run_regression
python -m tests.run_regression --verbose
python -m tests.run_regression -v
python -m tests.run_regression --quite
python -m tests.run_regression -q
"""
from tests.regression.regression_runner import main

if __name__ == "__main__":
    main()
