@echo off
echo Uninstalling Uni-Proxy Manager...

REM Remove from startup
python proxy_manager.py --remove-startup

echo.
echo Uni-Proxy Manager removed from startup.
echo You can manually delete this folder to completely remove the application.
echo.
pause
