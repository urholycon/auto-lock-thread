#!/usr/bin/env python3
"""
Automatic dependency installer for Discord Thread Auto-Lock Bot
"""
import subprocess
import sys
import importlib.util

def check_package(package_name):
    """Check if a package is installed"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_package(package):
    """Install a package using pip"""
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print(f"✅ {package} installed successfully")

def main():
    """Main dependency checker and installer"""
    required_packages = {
        'discord': 'discord.py>=2.3.0',
        'dotenv': 'python-dotenv>=1.0.0', 
        'flask': 'flask>=3.0.0',
        'aiohttp': 'aiohttp>=3.8.0',
        'requests': 'requests>=2.31.0'
    }
    
    print("🔍 Checking dependencies for Discord Thread Auto-Lock Bot...")
    
    missing_packages = []
    for import_name, pip_name in required_packages.items():
        if not check_package(import_name):
            missing_packages.append(pip_name)
        else:
            print(f"✅ {import_name} is already installed")
    
    if missing_packages:
        print(f"\n📦 Installing {len(missing_packages)} missing dependencies...")
        for package in missing_packages:
            try:
                install_package(package)
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
                return False
        print("\n🎉 All dependencies installed successfully!")
    else:
        print("\n✅ All dependencies are already installed!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)