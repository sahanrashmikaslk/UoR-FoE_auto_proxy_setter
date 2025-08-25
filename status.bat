@echo off
echo ====================================
echo  Uni-Proxy Manager v1.1 Status Check
echo ====================================
echo.

REM Check if Python is available
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python not found
) else (
    echo [✓] Python available
    python --version
)

echo.

REM Check if required packages are installed
echo Checking Python packages...
python -c "import pystray; print('[✓] pystray installed')" 2>nul || echo [X] pystray not installed
python -c "import PIL; print('[✓] Pillow installed')" 2>nul || echo [X] Pillow not installed  
python -c "import psutil; print('[✓] psutil installed')" 2>nul || echo [X] psutil not installed

echo.

REM Check if configuration exists
echo Checking configuration...
if exist "proxy_config.json" (
    echo [✓] Configuration file exists
) else (
    echo [X] Configuration file missing
)

echo.

REM Check if Git is available
echo Checking Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo [X] Git not found
) else (
    echo [✓] Git available
    git --version
)

echo.

REM Check current Git proxy setting
echo Checking Git proxy...
for /f "tokens=*" %%i in ('git config --global --get http.proxy 2^>nul') do (
    echo [✓] Git proxy: %%i
    goto git_done
)
echo [-] No Git proxy configured
:git_done

echo.

REM Check if npm is available
echo Checking npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo [X] npm not found
) else (
    echo [✓] npm available
    npm --version
)

echo.

REM Check current npm proxy setting  
echo Checking npm proxy...
for /f "tokens=*" %%i in ('npm config get proxy 2^>nul') do (
    if not "%%i"=="null" (
        echo [✓] npm proxy: %%i
    ) else (
        echo [-] No npm proxy configured
    )
    goto npm_done
)
echo [-] No npm proxy configured
:npm_done

echo.

REM Check VS Code settings
echo Checking VS Code...
if exist "%APPDATA%\Code\User\settings.json" (
    echo [✓] VS Code settings found
) else (
    echo [-] VS Code settings not found
)

echo.

REM Check Windows proxy status
echo Checking Windows proxy...
python -c "
import winreg
try:
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings')
    proxy_enable, _ = winreg.QueryValueEx(key, 'ProxyEnable')
    if proxy_enable:
        proxy_server, _ = winreg.QueryValueEx(key, 'ProxyServer')
        print(f'[✓] Windows proxy enabled: {proxy_server}')
    else:
        print('[-] Windows proxy disabled')
    winreg.CloseKey(key)
except:
    print('[X] Could not check Windows proxy')
"

echo.

REM Check if running at startup
echo Checking startup configuration...
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "UniProxyManager" >nul 2>&1
if errorlevel 1 (
    echo [-] Not configured to start with Windows
) else (
    echo [✓] Configured to start with Windows
)

echo.
echo Status check completed!
echo.
pause
