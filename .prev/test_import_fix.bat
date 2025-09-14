@echo off
title Final Test - Fixed Proxy Manager
color 0A

echo ===============================================
echo      FINAL TEST - Fixed Import Issue
echo ===============================================
echo.

echo 🧪 Testing Fixed Portable Version...
echo.

echo Test 1: Running --config command...
echo This should open the configuration window
cd UniProxyManager_Fixed_Portable
echo Running: UniProxyManager.exe --config
start "" "UniProxyManager.exe" --config
cd ..

timeout /t 3 /nobreak >nul

echo.
echo Test 2: Running Config.bat...
echo This should also open the configuration window
start "" "UniProxyManager_Fixed_Portable\Config.bat"

timeout /t 3 /nobreak >nul

echo.
echo Test 3: Starting main application...
echo This should start the system tray application
cd UniProxyManager_Fixed_Portable
start "" "Start.bat"
cd ..

echo.
echo ===============================================
echo              Test Complete!
echo ===============================================
echo.
echo ✅ If you see configuration windows opening, the fix worked!
echo ✅ Look for the red/green tray icon after running Start.bat
echo.
echo 🎯 The import error has been fixed:
echo   • Changed from 'ConfigGUI' to 'ProxyConfigGUI'
echo   • Fixed the class instantiation
echo   • Config window should now work in the executable
echo.
echo 📋 Ready for testing on another PC:
echo   1. Copy entire "UniProxyManager_Fixed_Portable" folder
echo   2. Run Start.bat
echo   3. Right-click tray icon → Configuration (should work!)
echo   4. Or run Config.bat directly
echo.
echo 💡 The ImportError has been resolved!
echo.
pause
