import sys
import os
import subprocess
import winreg
from pathlib import Path

def test_proxy_functions():
    """Test proxy manager functions without GUI"""
    print("Testing Proxy Manager Functions")
    print("=" * 40)
    
    # Import the proxy manager
    sys.path.append(str(Path(__file__).parent))
    from proxy_manager import ProxyManager
    
    # Create instance
    manager = ProxyManager()
    
    print(f"Proxy Server: {manager.proxy_server}")
    print(f"Proxy URL: {manager.proxy_url}")
    print(f"Initial Status: {'Enabled' if manager.is_proxy_enabled else 'Disabled'}")
    print()
    
    # Test Windows proxy check
    print("Testing Windows proxy status check...")
    manager.check_proxy_status()
    print(f"Windows proxy status: {'Enabled' if manager.is_proxy_enabled else 'Disabled'}")
    print()
    
    # Test configuration loading
    print("Testing configuration loading...")
    config = manager.load_config()
    print("Configuration loaded:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    print()
    
    # Test each proxy setting function (dry run)
    print("Testing proxy setting functions...")
    
    print("Testing Git proxy check...")
    try:
        result = subprocess.run(["git", "config", "--global", "--get", "http.proxy"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  Current Git proxy: {result.stdout.strip()}")
        else:
            print("  No Git proxy configured")
    except Exception as e:
        print(f"  Git not available: {e}")
    
    print("Testing npm proxy check...")
    try:
        result = subprocess.run(["npm", "config", "get", "proxy"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            proxy_value = result.stdout.strip()
            if proxy_value and proxy_value != "null":
                print(f"  Current npm proxy: {proxy_value}")
            else:
                print("  No npm proxy configured")
        else:
            print("  npm not available or no proxy set")
    except Exception as e:
        print(f"  npm not available: {e}")
    
    print("Testing VS Code settings path...")
    vscode_path = Path.home() / "AppData" / "Roaming" / "Code" / "User" / "settings.json"
    print(f"  VS Code settings path: {vscode_path}")
    print(f"  VS Code settings exists: {vscode_path.exists()}")
    
    print()
    print("All tests completed!")
    return True

if __name__ == "__main__":
    try:
        test_proxy_functions()
        print("\nProxy Manager test completed successfully!")
    except Exception as e:
        print(f"\nError during testing: {e}")
        sys.exit(1)
