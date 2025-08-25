@echo off
echo ====================================
echo       Uni-Proxy Manager v1.0
echo    Quick Setup Instructions
echo ====================================
echo.

if not exist "proxy_config.json" (
    echo First time setup detected!
    echo Running full installation...
    call install.bat
) else (
    echo Configuration found. Starting Uni-Proxy Manager...
    echo.
    echo Controls:
    echo - Look for red/green icon in system tray
    echo - Click icon to toggle proxy on/off  
    echo - Right-click for menu options
    echo.
    python proxy_manager.py
)

echo.
echo Available commands:
echo - install.bat   : Full installation
echo - config.bat    : Open configuration  
echo - run.bat       : Start application
echo - uninstall.bat : Remove from startup
echo.
pause
