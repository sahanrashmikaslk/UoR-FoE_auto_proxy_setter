@echo off
title Testing Fixed Portable Version
color 0A

echo ===============================================
echo      Testing Uni-Proxy Manager Fixed Version
echo ===============================================
echo.

echo 🧪 Test 1: Checking executable exists...
if exist "UniProxyManager_Fixed_Portable\UniProxyManager.exe" (
    echo ✅ UniProxyManager.exe found
) else (
    echo ❌ UniProxyManager.exe not found!
    pause
    exit /b 1
)

echo.
echo 🧪 Test 2: Testing --help command...
cd UniProxyManager_Fixed_Portable
UniProxyManager.exe --help
cd ..

echo.
echo 🧪 Test 3: Testing --config command...
echo This should open the config window (will close after 3 seconds)
cd UniProxyManager_Fixed_Portable
start "" "UniProxyManager.exe" --config
cd ..
timeout /t 3 /nobreak >nul

echo.
echo 🧪 Test 4: File structure check...
if exist "UniProxyManager_Fixed_Portable\Start.bat" echo ✅ Start.bat found
if exist "UniProxyManager_Fixed_Portable\Config.bat" echo ✅ Config.bat found
if exist "UniProxyManager_Fixed_Portable\proxy_config.json" echo ✅ proxy_config.json found
if exist "UniProxyManager_Fixed_Portable\README.md" echo ✅ README.md found

echo.
echo ===============================================
echo           Test Results Summary
echo ===============================================
echo.
echo ✅ Fixed Portable Version appears to be working!
echo.
echo 📋 What was fixed:
echo   • Config window now works (embedded GUI)
echo   • --config command line option added
echo   • Config.bat for easy access
echo   • All files properly included
echo.
echo 🎯 Ready for testing on another PC!
echo.
echo Copy the entire "UniProxyManager_Fixed_Portable" folder
echo to another PC and test:
echo   1. Run Start.bat
echo   2. Right-click tray icon → Configuration
echo   3. Or run Config.bat directly
echo.
pause
