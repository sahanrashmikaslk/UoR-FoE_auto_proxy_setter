@echo off
title Uni-Proxy Manager - Advanced Build System
color 0A

echo ===============================================
echo    Uni-Proxy Manager Advanced Build System
echo ===============================================
echo.

REM Check for virtual environment
if not exist ".venv" (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv .venv
    echo Then: .venv\Scripts\activate
    echo Then: pip install -r requirements.txt
    pause
    exit /b 1
)

echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo 📋 Build Options:
echo [1] Fixed Portable Version (config window works)
echo [2] Single Installer Executable  
echo [3] Both (Recommended)
echo.
set /p choice="Choose option (1-3): "

if "%choice%"=="1" goto build_portable
if "%choice%"=="2" goto build_installer  
if "%choice%"=="3" goto build_both
echo ❌ Invalid choice!
pause
exit /b 1

:build_both
echo.
echo 🚀 Building both versions...
call :build_portable
call :build_installer
goto done

:build_portable
echo.
echo ====================================
echo   Building Fixed Portable Version
echo ====================================
echo.

echo 🔧 Building fixed executable with embedded config...
pyinstaller --onefile --noconsole --icon=NONE ^
    --add-data "proxy_config.json;." ^
    --add-data "config_gui.py;." ^
    --name "UniProxyManager_Fixed" ^
    --distpath "dist_fixed" ^
    proxy_manager.py

if errorlevel 1 (
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo.
echo 📦 Creating fixed portable package...

REM Clean up old portable folder
if exist "UniProxyManager_Fixed_Portable" rmdir /s /q "UniProxyManager_Fixed_Portable"
mkdir "UniProxyManager_Fixed_Portable"

REM Copy files
copy "dist_fixed\UniProxyManager_Fixed.exe" "UniProxyManager_Fixed_Portable\UniProxyManager.exe"
copy "proxy_config.json" "UniProxyManager_Fixed_Portable\"
copy "README.md" "UniProxyManager_Fixed_Portable\"

REM Create improved start script
echo @echo off > "UniProxyManager_Fixed_Portable\Start.bat"
echo echo Starting Uni-Proxy Manager (Fixed Version)... >> "UniProxyManager_Fixed_Portable\Start.bat"
echo start "" "UniProxyManager.exe" >> "UniProxyManager_Fixed_Portable\Start.bat"
echo echo Application started! Check your system tray. >> "UniProxyManager_Fixed_Portable\Start.bat"

REM Create config launcher
echo @echo off > "UniProxyManager_Fixed_Portable\Config.bat"
echo echo Opening Configuration Window... >> "UniProxyManager_Fixed_Portable\Config.bat"
echo start "" "UniProxyManager.exe" --config >> "UniProxyManager_Fixed_Portable\Config.bat"

echo.
echo ✅ Fixed portable version created in: UniProxyManager_Fixed_Portable\
goto :eof

:build_installer
echo.
echo ====================================
echo   Building Single Installer
echo ====================================
echo.

echo 🔧 Building installer executable...
pyinstaller --onefile --noconsole --icon=NONE ^
    --add-data "proxy_config.json;." ^
    --add-data "config_gui.py;." ^
    --add-data "dist_fixed\UniProxyManager_Fixed.exe;." ^
    --add-data "README.md;." ^
    --name "UniProxyManager_Installer" ^
    --distpath "dist_installer" ^
    installer.py

if errorlevel 1 (
    echo ❌ Installer build failed!
    pause
    exit /b 1
)

echo.
echo ✅ Single installer created: dist_installer\UniProxyManager_Installer.exe
goto :eof

:done
echo.
echo ====================================
echo       Build Complete! 
echo ====================================
echo.
echo 📁 Files Created:
echo.
if exist "UniProxyManager_Fixed_Portable" (
    echo ✅ Fixed Portable Version:
    echo    📂 UniProxyManager_Fixed_Portable\
    echo       📄 UniProxyManager.exe ^(Config window works!^)
    echo       📄 Start.bat
    echo       📄 Config.bat  
    echo       📄 proxy_config.json
    echo       📄 README.md
    echo.
)
if exist "dist_installer\UniProxyManager_Installer.exe" (
    echo ✅ Single Installer:
    echo    📄 dist_installer\UniProxyManager_Installer.exe
    echo       ^(Complete installer with GUI^)
    echo.
)

echo 🎯 Testing Recommendations:
echo.
echo 1. Fixed Portable Version:
echo    - Copy "UniProxyManager_Fixed_Portable" folder to test PC
echo    - Run "Start.bat" or "UniProxyManager.exe"
echo    - Right-click tray icon → Configuration (should work now!)
echo.
echo 2. Single Installer:  
echo    - Copy "UniProxyManager_Installer.exe" to test PC
echo    - Run it and follow installation wizard
echo    - Choose Standard or Portable installation
echo.
echo ✨ Config window issue is now fixed in both versions!
echo.
pause
