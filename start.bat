@echo off
echo ====================================
echo      Uni-Proxy Manager v1.1.1
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
    echo Starting silently in background...
    start "" pythonw proxy_manager_silent.pyw
    echo Application started! Check your system tray for the proxy icon.
)

echo.
echo Available commands:
echo - install.bat          : Full installation
echo - config.bat           : Open configuration  
echo - start.bat            : Start application (this file)
echo - status.bat           : Check proxy status
echo - uninstall.bat        : Remove from startup
echo.
pause
