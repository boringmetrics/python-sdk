#!/usr/bin/env python3
"""
Build script for the Boring Metrics Python SDK
"""

import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path


def clean():
    """Clean build artifacts"""
    print("Cleaning build artifacts...")

    dirs_to_clean = [
        "dist",
        "build",
        "boringmetrics.egg-info",
        "__pycache__",
        "boringmetrics/__pycache__",
        ".build-venv",  # Add the virtual environment to clean
    ]

    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name}...")
            shutil.rmtree(dir_name)


def create_venv():
    """Create a virtual environment for building"""
    print("Creating virtual environment for building...")
    venv_dir = ".build-venv"
    venv.create(venv_dir, with_pip=True)

    # Get the path to the Python executable in the virtual environment
    if sys.platform == "win32":
        venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        venv_python = os.path.join(venv_dir, "bin", "python")

    return venv_python


def build(venv_python):
    """Build the package"""
    print("Building package...")

    # Make sure we have the latest build tools in the virtual environment
    subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "setuptools", "wheel", "build"])

    # Build the package
    subprocess.check_call([venv_python, "-m", "build"])

    print("Build completed successfully!")


def main():
    """Main entry point"""
    # Change to the project root directory
    os.chdir(Path(__file__).parent.parent)

    clean()
    venv_python = create_venv()
    build(venv_python)


if __name__ == "__main__":
    main()
