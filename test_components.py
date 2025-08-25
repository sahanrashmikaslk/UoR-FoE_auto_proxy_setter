import sys
import threading
import time
from pathlib import Path

# Test system tray functionality
def test_system_tray():
    print("Testing System Tray Functionality")
    print("=" * 40)
    
    try:
        # Import required modules
        import pystray
        from PIL import Image, ImageDraw
        print("✓ pystray and PIL imported successfully")
        
        # Test icon creation
        image = Image.new('RGB', (64, 64), (255, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rectangle([10, 10, 54, 54], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
        draw.text((18, 25), "TEST", fill=(0, 0, 0))
        print("✓ Icon creation successful")
        
        # Test menu creation
        def dummy_action():
            print("Menu item clicked!")
        
        menu = pystray.Menu(
            pystray.MenuItem("Test Item", dummy_action),
            pystray.MenuItem("Quit", dummy_action)
        )
        print("✓ Menu creation successful")
        
        # Test icon initialization (don't run it)
        icon = pystray.Icon("Test", image, "Test Icon", menu=menu)
        print("✓ Icon initialization successful")
        
        print("\n✓ All system tray components working correctly!")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_proxy_manager_import():
    print("\nTesting Proxy Manager Import")
    print("=" * 40)
    
    try:
        # Test importing the main module
        sys.path.append(str(Path(__file__).parent))
        from proxy_manager import ProxyManager
        print("✓ ProxyManager imported successfully")
        
        # Test creating instance
        manager = ProxyManager()
        print("✓ ProxyManager instance created")
        print(f"  Proxy Server: {manager.proxy_server}")
        print(f"  Proxy URL: {manager.proxy_url}")
        print(f"  Current Status: {'Enabled' if manager.is_proxy_enabled else 'Disabled'}")
        
        # Test configuration loading
        config = manager.config
        print("✓ Configuration loaded successfully")
        print(f"  Windows: {config.get('enable_windows', 'N/A')}")
        print(f"  Git: {config.get('enable_git', 'N/A')}")
        print(f"  npm: {config.get('enable_npm', 'N/A')}")
        print(f"  VS Code: {config.get('enable_vscode', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("Proxy Manager Component Test")
    print("=" * 50)
    
    # Test system tray functionality
    tray_ok = test_system_tray()
    
    # Test proxy manager
    manager_ok = test_proxy_manager_import()
    
    print("\n" + "=" * 50)
    if tray_ok and manager_ok:
        print("✓ ALL TESTS PASSED!")
        print("\nThe Proxy Manager should work correctly.")
        print("You can now run: python proxy_manager.py")
    else:
        print("✗ SOME TESTS FAILED!")
        print("Please check the error messages above.")
    
    print("=" * 50)
