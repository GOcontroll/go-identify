#!/usr/bin/env python3

from setuptools import setup, Extension
from pathlib import Path

root = Path(__file__).parent
long_description = (root / "README.md").read_text()

setup(
        name="go-identify",
        version="1.0.0",
        description="A small script to print some info and flash leds if available",
        url="https://github.com/GOcontroll/go-identify",
        author="Maud Spierings",
        author_email="maudspierings@gocontroll.com",
        license="MIT",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=["go_identify"],
        install_requires=[],
        entry_points={
            "console_scripts": [
                "identify = go_identify.identify:identify",
            ]
        },
        python_requires=">=3.9",
)
