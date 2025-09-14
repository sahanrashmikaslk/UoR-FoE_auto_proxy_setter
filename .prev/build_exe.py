#!/usr/bin/env python3
"""
Build script to create executable for Uni-Proxy Manager
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building Uni-Proxy Manager Executable...")
    print("=" * 50)
    
    # Clean previous builds
    build_dirs = ['build', 'dist', '__pycache__']
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            print(f"🧹 Cleaning {dir_name}...")
            shutil.rmtree(dir_name, ignore_errors=True)
    
    # Remove old spec files
    spec_files = [f for f in os.listdir('.') if f.endswith('.spec')]
    for spec_file in spec_files:
        os.remove(spec_file)
        print(f"🗑️ Removed {spec_file}")
    
    print("\n📦 Creating executable...")
    
    # PyInstaller command to create executable
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',                    # Single executable file
        '--windowed',                   # No console window
        '--name=UniProxyManager',       # Name of executable
        '--icon=NONE',                  # No icon for now
        '--add-data=proxy_config.json;.',  # Include config file
        '--add-data=config_gui.py;.',   # Include GUI module
        '--hidden-import=pystray',      # Ensure pystray is included
        '--hidden-import=PIL',          # Ensure PIL is included
        '--hidden-import=tkinter',      # Ensure tkinter is included
        'proxy_manager.py'              # Main script
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Executable created successfully!")
        
        # Check if executable was created
        exe_path = Path('dist/UniProxyManager.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📁 Executable size: {size_mb:.1f} MB")
            print(f"📍 Location: {exe_path.absolute()}")
            
            # Create distribution folder with all necessary files
            create_distribution()
            
        else:
            print("❌ Executable not found!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print("Error output:", e.stderr)
        return False
    
    return True

def create_distribution():
    """Create a distribution folder with executable and support files"""
    print("\n📦 Creating distribution package...")
    
    dist_folder = Path('UniProxyManager_Portable')
    
    # Clean and create distribution folder
    if dist_folder.exists():
        shutil.rmtree(dist_folder)
    dist_folder.mkdir()
    
    # Copy executable
    shutil.copy2('dist/UniProxyManager.exe', dist_folder / 'UniProxyManager.exe')
    
    # Copy essential files
    essential_files = [
        'proxy_config.json',
        'requirements.txt',
        'README.md'
    ]
    
    for file_name in essential_files:
        if os.path.exists(file_name):
            shutil.copy2(file_name, dist_folder / file_name)
    
    # Create batch files for distribution
    create_portable_batch_files(dist_folder)
    
    print(f"✅ Portable distribution created in: {dist_folder.absolute()}")
    print("\n📋 Distribution contents:")
    for item in dist_folder.iterdir():
        if item.is_file():
            size_kb = item.stat().st_size / 1024
            print(f"   📄 {item.name} ({size_kb:.1f} KB)")

def create_portable_batch_files(dist_folder):
    """Create simplified batch files for portable version"""
    
    # Start script
    start_script = """@echo off
echo ====================================
echo    Uni-Proxy Manager v1.1.1
echo         Portable Version
echo ====================================
echo.
echo Starting Uni-Proxy Manager...
echo Look for the proxy icon in your system tray.
echo.
start "" "UniProxyManager.exe"
echo.
echo Application started! Check your system tray.
echo Close this window - the application runs in background.
echo.
pause
"""
    
    # Config script
    config_script = """@echo off
echo Opening configuration...
start "" "UniProxyManager.exe" --config
"""
    
    # Status script
    status_script = """@echo off
echo ====================================
echo    Uni-Proxy Manager Status
echo ====================================
echo.
echo Current Status:
"UniProxyManager.exe" --status
echo.
pause
"""
    
    # Install script for portable version
    install_script = """@echo off
echo ====================================
echo   Uni-Proxy Manager Installer
echo        Portable Version
echo ====================================
echo.
echo This will add Uni-Proxy Manager to Windows startup.
echo.
choice /M "Add to Windows startup"
if errorlevel 2 goto end
echo.
echo Adding to startup...
"UniProxyManager.exe" --add-startup
echo.
echo Done! The application will start with Windows.
echo.
:end
pause
"""
    
    # Write batch files
    batch_files = {
        'Start.bat': start_script,
        'Config.bat': config_script,
        'Status.bat': status_script,
        'Install.bat': install_script
    }
    
    for filename, content in batch_files.items():
        with open(dist_folder / filename, 'w') as f:
            f.write(content)

if __name__ == "__main__":
    print("🚀 Uni-Proxy Manager Build System")
    print("=" * 50)
    
    if build_executable():
        print("\n🎉 Build completed successfully!")
        print("\n📋 Next steps:")
        print("1. Test the executable: dist/UniProxyManager.exe")
        print("2. Use portable version: UniProxyManager_Portable/")
        print("3. Distribute the portable folder to other PCs")
    else:
        print("\n❌ Build failed!")
        sys.exit(1)
