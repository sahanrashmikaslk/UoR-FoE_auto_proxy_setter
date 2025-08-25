@echo off
echo Uninstalling Proxy Manager...

REM Remove from startup
python proxy_manager.py --remove-startup

echo.
echo Proxy Manager removed from startup.
echo You can manually delete this folder to completely remove the application.
echo.
pause
