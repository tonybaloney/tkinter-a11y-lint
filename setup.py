#!/usr/bin/env python3
"""Setup script for tkinter-a11y-lint."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tkinter-a11y-lint",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A pylint plugin for tkinter accessibility linting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tkinter-a11y-lint",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pylint>=2.15.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    entry_points={
        "pylint.plugins": [
            "tkinter_a11y = tkinter_a11y_lint.plugin",
        ],
    },
)