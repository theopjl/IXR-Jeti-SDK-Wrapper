"""
JETI SDK Python Wrapper - Package Setup

This module provides backward compatibility for editable installs
and serves as an alternative entry point.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="jeti-sdk-wrapper",
    version="1.0.0",
    description="Python wrapper for JETI SDK for radiometric and spectroscopic measurements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="JETI SDK Wrapper",
    license="MIT",
    python_requires=">=3.11",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "ruff>=0.1.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "Typing :: Typed",
    ],
    keywords=[
        "jeti",
        "sdk",
        "spectroscopy",
        "radiometry",
        "colorimetry",
        "light measurement",
        "spectral analysis",
    ],
)
