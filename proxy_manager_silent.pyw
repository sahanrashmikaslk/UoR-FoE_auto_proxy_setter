#!/usr/bin/env python3
"""
Uni-Proxy Manager - Silent Launcher
Runs the proxy manager without showing console window
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch proxy manager silently"""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    proxy_manager_path = script_dir / "proxy_manager.py"
    
    # Check if proxy_manager.py exists
    if not proxy_manager_path.exists():
        print(f"Error: {proxy_manager_path} not found!")
        return 1
    
    try:
        # Start the proxy manager without showing console window
        if os.name == 'nt':  # Windows
            # Use CREATE_NO_WINDOW flag to hide console
            subprocess.Popen([
                sys.executable, 
                str(proxy_manager_path)
            ], creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            # For other systems, just run normally
            subprocess.Popen([sys.executable, str(proxy_manager_path)])
        
        print("Uni-Proxy Manager started successfully in background")
        return 0
        
    except Exception as e:
        print(f"Error starting Uni-Proxy Manager: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
