#!/usr/bin/env python3
"""
Release script for the Boring Metrics Python SDK
"""

import os
import subprocess
import sys
from pathlib import Path


def check_twine():
    """Check if twine is installed"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "show", "twine"], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Installing twine...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "twine"])


def build():
    """Build the package"""
    print("Building package...")
    
    # Run the build script
    build_script = Path(__file__).parent / "build.py"
    subprocess.check_call([sys.executable, str(build_script)])


def check_api_token():
    """Check if PyPI API token is set"""
    if not os.environ.get("TWINE_API_TOKEN"):
        # Try to load from .env.local if it exists
        env_file = Path(__file__).parent.parent / ".env.local"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.strip() and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        if key == "TWINE_API_TOKEN":
                            os.environ[key] = value
        
        # Check again after trying to load from .env.local
        if not os.environ.get("TWINE_API_TOKEN"):
            print("Error: TWINE_API_TOKEN environment variable is not set.")
            print("Please set it or create a .env.local file with TWINE_API_TOKEN=your-token")
            sys.exit(1)


def upload_to_pypi():
    """Upload the package to PyPI"""
    print("Uploading to PyPI...")
    
    # Check if API token is set
    check_api_token()
    
    # Upload to PyPI
    subprocess.check_call([sys.executable, "-m", "twine", "upload", "dist/*"])
    
    print("Package uploaded to PyPI successfully!")


def main():
    """Main entry point"""
    # Change to the project root directory
    os.chdir(Path(__file__).parent.parent)
    
    check_twine()
    build()
    
    # Confirm before uploading
    response = input("Do you want to upload the package to PyPI? (y/N): ")
    if response.lower() == "y":
        upload_to_pypi()
    else:
        print("Upload cancelled.")


if __name__ == "__main__":
    main()
