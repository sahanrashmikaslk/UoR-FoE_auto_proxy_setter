@echo off
REM Start Uni-Proxy Manager silently in background without console window
python -c "import subprocess, sys; subprocess.Popen([sys.executable, 'proxy_manager.py'], creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)"
