#!/usr/bin/env python3
"""
Build script for the Boring Metrics Python SDK
"""

import os
import shutil
import subprocess
import sys
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
    ]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name}...")
            shutil.rmtree(dir_name)


def build():
    """Build the package"""
    print("Building package...")
    
    # Make sure we have the latest build tools
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "setuptools", "wheel", "build"])
    
    # Build the package
    subprocess.check_call([sys.executable, "-m", "build"])
    
    print("Build completed successfully!")


def main():
    """Main entry point"""
    # Change to the project root directory
    os.chdir(Path(__file__).parent.parent)
    
    clean()
    build()


if __name__ == "__main__":
    main()
