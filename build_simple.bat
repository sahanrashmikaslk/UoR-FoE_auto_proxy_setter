@echo off
echo ====================================
echo  Uni-Proxy Manager Build System
echo ====================================
echo.
echo Building executable with PyInstaller...
echo.

REM Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec"

echo Creating single executable file...
C:\Users\sahan\Desktop\MYProjects\UoR-FoE_auto_proxy_setter\.venv\Scripts\python.exe -m PyInstaller ^
  --onefile ^
  --windowed ^
  --name=UniProxyManager ^
  --add-data="proxy_config.json;." ^
  --hidden-import=pystray ^
  --hidden-import=PIL ^
  --hidden-import=tkinter ^
  proxy_manager.py

if exist "dist\UniProxyManager.exe" (
    echo.
    echo ✅ Executable created successfully!
    echo 📁 Location: dist\UniProxyManager.exe
    
    REM Create portable distribution
    if exist "UniProxyManager_Portable" rmdir /s /q "UniProxyManager_Portable"
    mkdir "UniProxyManager_Portable"
    
    copy "dist\UniProxyManager.exe" "UniProxyManager_Portable\"
    copy "proxy_config.json" "UniProxyManager_Portable\"
    copy "README.md" "UniProxyManager_Portable\"
    
    REM Create simple start script for portable version
    echo @echo off > "UniProxyManager_Portable\Start.bat"
    echo echo Starting Uni-Proxy Manager... >> "UniProxyManager_Portable\Start.bat"
    echo start "" "UniProxyManager.exe" >> "UniProxyManager_Portable\Start.bat"
    echo echo Application started! Check your system tray. >> "UniProxyManager_Portable\Start.bat"
    
    echo.
    echo 📦 Portable version created in: UniProxyManager_Portable\
    echo.
    echo 🎉 Build completed successfully!
    echo.
    echo 📋 Files created:
    dir /b "UniProxyManager_Portable"
    
) else (
    echo.
    echo ❌ Build failed! Executable not found.
)

echo.
pause
