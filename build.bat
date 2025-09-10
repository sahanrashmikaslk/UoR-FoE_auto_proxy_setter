@echo off
echo ====================================
echo  Uni-Proxy Manager Build System
echo ====================================
echo.
echo This will create a portable executable file.
echo.
pause

echo Building executable...
python build_exe.py

echo.
echo Build complete! Check the results above.
pause
