@echo ====================================
echo   Uni-Proxy Manager v1.1 Installer
echo ====================================o off
echo ====================================
echo    Uni-Proxy Manager Installer
echo ====================================

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

python --version
echo Python found!

REM Check if pip is available
echo Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not available
    echo Please install pip or reinstall Python with pip included
    pause
    exit /b 1
)

echo pip found!

REM Install requirements
echo.
echo Installing required packages...
echo This may take a few minutes...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Error: Failed to install requirements
    echo Please check your internet connection and try again
    echo If you're behind a proxy, you may need to configure pip first
    pause
    exit /b 1
)

echo.
echo All packages installed successfully!

REM Create initial configuration
echo Creating default configuration...
python -c "import json; config = {'proxy_server': '10.50.225.222', 'proxy_port': '3128', 'auto_start': True, 'enable_windows': True, 'enable_git': True, 'enable_npm': True, 'enable_vscode': True}; json.dump(config, open('proxy_config.json', 'w'), indent=4); print('Configuration file created!')"

REM Add to startup
echo.
echo Adding to Windows startup...
python proxy_manager.py --add-startup

echo.
echo ====================================
echo    Installation Complete!
echo ====================================
echo.
echo The Uni-Proxy Manager v1.1 has been installed successfully!
echo.
echo What's new in v1.1:
echo - Fixed npm error handling
echo - Modern round system tray icons
echo - Improved UI design
echo - Better error reporting
echo.
echo What's next:
echo 1. The application will start automatically with Windows
echo 2. Look for the proxy icon in your system tray (red/green circle)
echo 3. Click the icon to toggle proxy on/off
echo 4. Right-click for more options including configuration
echo.
echo Manual controls:
echo - start.bat        : Start the application manually
echo - start_silent.bat : Start silently without console window  
echo - config.bat       : Open configuration window
echo - uninstall.bat    : Remove from startup
echo.
echo Icon indicators:
echo - Green = Proxy enabled
echo - Red   = Proxy disabled
echo.
echo Starting the application now...
start "" pythonw proxy_manager_silent.pyw

echo.
echo The application is now running silently in the background!
echo Look for the proxy icon in your system tray.
echo.
pause
