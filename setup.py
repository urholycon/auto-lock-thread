#!/usr/bin/env python3
"""
Setup script for Discord Thread Auto-Lock Bot
Complete deployment automation
"""
import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'handlers', 'utils']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")

def check_environment():
    """Check if DISCORD_TOKEN is set"""
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("⚠️  DISCORD_TOKEN not found in environment")
        print("   Please add your Discord bot token to Replit Secrets")
        return False
    print("✅ Discord token found in environment")
    return True

def run_dependency_check():
    """Run the dependency installer"""
    print("\n🔧 Running dependency check...")
    try:
        result = subprocess.run([sys.executable, "install_deps.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependencies check completed")
            return True
        else:
            print(f"❌ Dependency check failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running dependency check: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Discord Thread Auto-Lock Bot Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    print("\n📁 Setting up directories...")
    create_directories()
    
    # Check dependencies
    if not run_dependency_check():
        sys.exit(1)
    
    # Check environment
    print("\n🔑 Checking environment...")
    token_ok = check_environment()
    
    print("\n" + "=" * 40)
    print("📋 Setup Summary:")
    print("✅ Python version compatible")
    print("✅ Directories created")
    print("✅ Dependencies installed")
    
    if token_ok:
        print("✅ Discord token configured")
        print("\n🎉 Setup complete! Your bot is ready to run.")
        print("   Execute: python main.py")
    else:
        print("⚠️  Discord token missing")
        print("\n⚠️  Setup incomplete. Please add DISCORD_TOKEN to environment.")
        print("   Then run: python main.py")
    
    return token_ok

if __name__ == "__main__":
    main()