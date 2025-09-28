#!/usr/bin/env python3
"""Test script to demonstrate the tkinter accessibility plugin."""

import os
import subprocess
import sys


def run_pylint_on_examples():
    """Run pylint on the example files to demonstrate the plugin."""

    print("Testing tkinter-a11y-lint plugin...")
    print("=" * 50)

    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Test files
    bad_example = os.path.join(current_dir, "examples", "bad_example.py")
    good_example = os.path.join(current_dir, "examples", "good_example.py")

    print("\n1. Testing BAD example (should show accessibility issues):")
    print("-" * 50)

    try:
        # Run pylint with our plugin on the bad example
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pylint",
                "--load-plugins=tkinter_a11y_lint.plugin",
                "--disable=all",
                "--enable=missing-text-attribute,missing-tab-index",
                bad_example,
            ],
            capture_output=True,
            text=True,
        )

        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr)
        print(f"Return code: {result.returncode}")

    except Exception as e:
        print(f"Error running pylint on bad example: {e}")

    print("\n2. Testing GOOD example (should show no accessibility issues):")
    print("-" * 50)

    try:
        # Run pylint with our plugin on the good example
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pylint",
                "--load-plugins=tkinter_a11y_lint.plugin",
                "--disable=all",
                "--enable=missing-text-attribute,missing-tab-index",
                good_example,
            ],
            capture_output=True,
            text=True,
        )

        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr)
        print(f"Return code: {result.returncode}")

    except Exception as e:
        print(f"Error running pylint on good example: {e}")


if __name__ == "__main__":
    run_pylint_on_examples()
