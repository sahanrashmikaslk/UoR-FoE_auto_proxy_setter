import os
import sys
import subprocess
import winreg
import json
import threading
import time
from pathlib import Path
import pystray
from PIL import Image, ImageDraw
import psutil

class ProxyManager:
    VERSION = "1.1.1"
    
    def __init__(self):
        # Load configuration
        self.config = self.load_config()
        
        self.proxy_server = f"{self.config['proxy_server']}:{self.config['proxy_port']}"
        self.proxy_url = f"http://{self.proxy_server}"
        self.is_proxy_enabled = False
        self.icon = None
        
        # Check initial proxy status
        self.check_proxy_status()
    
    def load_config(self):
        """Load configuration from file"""
        config_file = Path(__file__).parent / "proxy_config.json"
        default_config = {
            "proxy_server": "10.50.225.222",
            "proxy_port": "3128",
            "auto_start": True,
            "enable_windows": True,
            "enable_git": True,
            "enable_npm": True,
            "enable_vscode": True
        }
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    default_config.update(config)
                    return default_config
            except:
                return default_config
        return default_config
    
    def check_proxy_status(self):
        """Check if proxy is currently enabled in Windows settings"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
            proxy_enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
            winreg.CloseKey(key)
            self.is_proxy_enabled = bool(proxy_enable)
        except Exception:
            self.is_proxy_enabled = False
    
    def create_icon_image(self, color):
        """Create modern round system tray icon"""
        # Create a larger image for better quality
        size = 64
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))  # Transparent background
        draw = ImageDraw.Draw(image)
        
        # Calculate circle dimensions with padding
        padding = 6
        circle_size = size - (padding * 2)
        
        # Main circle (outer ring)
        outer_circle = [padding, padding, padding + circle_size, padding + circle_size]
        
        if color == (0, 255, 0):  # Green for enabled
            # Draw outer ring
            draw.ellipse(outer_circle, fill=(34, 197, 94), outline=(22, 163, 74), width=2)
            
            # Draw inner circle
            inner_padding = padding + 8
            inner_circle = [inner_padding, inner_padding, 
                          size - inner_padding, size - inner_padding]
            draw.ellipse(inner_circle, fill=(34, 197, 94))
            
            # Draw checkmark or "ON" indicator
            center_x, center_y = size // 2, size // 2
            # Draw a simple dot to indicate "ON"
            dot_size = 6
            dot_coords = [center_x - dot_size, center_y - dot_size,
                         center_x + dot_size, center_y + dot_size]
            draw.ellipse(dot_coords, fill=(255, 255, 255))
            
        else:  # Red for disabled
            # Draw outer ring
            draw.ellipse(outer_circle, fill=(239, 68, 68), outline=(220, 38, 38), width=2)
            
            # Draw inner circle
            inner_padding = padding + 8
            inner_circle = [inner_padding, inner_padding, 
                          size - inner_padding, size - inner_padding]
            draw.ellipse(inner_circle, fill=(239, 68, 68))
            
            # Draw "X" or "OFF" indicator
            center_x, center_y = size // 2, size // 2
            line_length = 8
            # Draw X
            draw.line([center_x - line_length, center_y - line_length,
                      center_x + line_length, center_y + line_length], 
                     fill=(255, 255, 255), width=3)
            draw.line([center_x + line_length, center_y - line_length,
                      center_x - line_length, center_y + line_length], 
                     fill=(255, 255, 255), width=3)
        
        return image
    
    def set_windows_proxy(self, enable=True):
        """Set Windows system proxy settings"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 
                               0, winreg.KEY_SET_VALUE)
            
            if enable:
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, self.proxy_server)
                winreg.SetValueEx(key, "ProxyOverride", 0, winreg.REG_SZ, "localhost;127.*;10.*;172.16.*;172.17.*;172.18.*;172.19.*;172.20.*;172.21.*;172.22.*;172.23.*;172.24.*;172.25.*;172.26.*;172.27.*;172.28.*;172.29.*;172.30.*;172.31.*;192.168.*")
            else:
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
                winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, "")
            
            winreg.CloseKey(key)
            
            # Refresh internet settings
            import ctypes
            wininet = ctypes.windll.wininet
            wininet.InternetSetOptionW(0, 37, 0, 0)  # INTERNET_OPTION_SETTINGS_CHANGED
            wininet.InternetSetOptionW(0, 39, 0, 0)  # INTERNET_OPTION_REFRESH
            
            return True
        except Exception as e:
            print(f"Error setting Windows proxy: {e}")
            return False
    
    def set_git_proxy(self, enable=True):
        """Set Git proxy configuration"""
        try:
            if enable:
                subprocess.run(["git", "config", "--global", "http.proxy", self.proxy_url], 
                             check=True, capture_output=True)
                subprocess.run(["git", "config", "--global", "https.proxy", self.proxy_url], 
                             check=True, capture_output=True)
            else:
                subprocess.run(["git", "config", "--global", "--unset", "http.proxy"], 
                             check=True, capture_output=True)
                subprocess.run(["git", "config", "--global", "--unset", "https.proxy"], 
                             check=True, capture_output=True)
            return True
        except Exception as e:
            print(f"Error setting Git proxy: {e}")
            return False
    
    def set_npm_proxy(self, enable=True):
        """Set npm proxy configuration"""
        try:
            # First check if npm is available
            result = subprocess.run(["npm", "--version"], 
                                   capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                print("npm not available, skipping npm proxy configuration")
                return True
            
            if enable:
                subprocess.run(["npm", "config", "set", "proxy", self.proxy_url], 
                             check=True, capture_output=True, timeout=30)
                subprocess.run(["npm", "config", "set", "https-proxy", self.proxy_url], 
                             check=True, capture_output=True, timeout=30)
            else:
                # Use delete with --ignore-errors to avoid errors if keys don't exist
                subprocess.run(["npm", "config", "delete", "proxy"], 
                             capture_output=True, timeout=30)
                subprocess.run(["npm", "config", "delete", "https-proxy"], 
                             capture_output=True, timeout=30)
            return True
        except subprocess.TimeoutExpired:
            print("npm command timed out, skipping npm proxy configuration")
            return True
        except FileNotFoundError:
            print("npm not installed, skipping npm proxy configuration")
            return True
        except Exception as e:
            print(f"npm proxy configuration skipped: {e}")
            return True  # Return True to not fail the entire operation
    
    def set_vscode_proxy(self, enable=True):
        """Set VS Code proxy configuration"""
        try:
            # VS Code settings path
            vscode_settings_path = Path.home() / "AppData" / "Roaming" / "Code" / "User" / "settings.json"
            
            if not vscode_settings_path.parent.exists():
                vscode_settings_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Read existing settings
            settings = {}
            if vscode_settings_path.exists():
                try:
                    with open(vscode_settings_path, 'r', encoding='utf-8') as f:
                        settings = json.load(f)
                except:
                    settings = {}
            
            # Update proxy settings
            if enable:
                settings["http.proxy"] = self.proxy_url
                settings["http.proxyStrictSSL"] = False
            else:
                settings.pop("http.proxy", None)
                settings.pop("http.proxyStrictSSL", None)
            
            # Write settings back
            with open(vscode_settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error setting VS Code proxy: {e}")
            return False
    
    def enable_proxy(self):
        """Enable proxy for all applications"""
        print("Enabling proxy...")
        
        results = []
        if self.config.get('enable_windows', True):
            results.append(("Windows", self.set_windows_proxy(True)))
        if self.config.get('enable_git', True):
            results.append(("Git", self.set_git_proxy(True)))
        if self.config.get('enable_npm', True):
            results.append(("npm", self.set_npm_proxy(True)))
        if self.config.get('enable_vscode', True):
            results.append(("VS Code", self.set_vscode_proxy(True)))
        
        self.is_proxy_enabled = True
        self.update_icon()
        
        # Show notification with modern styling
        if self.icon:
            success_count = sum(1 for _, success in results if success)
            total_count = len(results)
            if success_count == total_count:
                self.icon.notify("✅ Proxy enabled successfully!", f"Uni-Proxy Manager v{self.VERSION}")
            else:
                self.icon.notify(f"⚠️ Proxy enabled ({success_count}/{total_count} apps)", f"Uni-Proxy Manager v{self.VERSION}")
        
        return results
    
    def disable_proxy(self):
        """Disable proxy for all applications"""
        print("Disabling proxy...")
        
        results = []
        if self.config.get('enable_windows', True):
            results.append(("Windows", self.set_windows_proxy(False)))
        if self.config.get('enable_git', True):
            results.append(("Git", self.set_git_proxy(False)))
        if self.config.get('enable_npm', True):
            results.append(("npm", self.set_npm_proxy(False)))
        if self.config.get('enable_vscode', True):
            results.append(("VS Code", self.set_vscode_proxy(False)))
        
        self.is_proxy_enabled = False
        self.update_icon()
        
        # Show notification with modern styling
        if self.icon:
            success_count = sum(1 for _, success in results if success)
            total_count = len(results)
            if success_count == total_count:
                self.icon.notify("🔴 Proxy disabled successfully!", f"Uni-Proxy Manager v{self.VERSION}")
            else:
                self.icon.notify(f"⚠️ Proxy disabled ({success_count}/{total_count} apps)", f"Uni-Proxy Manager v{self.VERSION}")
        
        return results
    
    def toggle_proxy(self):
        """Toggle proxy on/off"""
        if self.is_proxy_enabled:
            self.disable_proxy()
        else:
            self.enable_proxy()
    
    def update_icon(self):
        """Update system tray icon based on proxy status"""
        if self.icon:
            color = (0, 255, 0) if self.is_proxy_enabled else (255, 0, 0)
            self.icon.icon = self.create_icon_image(color)
    
    def check_status(self):
        """Check and return current proxy status"""
        self.check_proxy_status()
        status = "Enabled" if self.is_proxy_enabled else "Disabled"
        status_icon = "🟢" if self.is_proxy_enabled else "🔴"
        if self.icon:
            self.icon.notify(f"{status_icon} Proxy Status: {status}", f"Uni-Proxy Manager v{self.VERSION}")
    
    def quit_app(self):
        """Quit the application"""
        if self.icon:
            self.icon.stop()
    
    def open_config(self):
        """Open configuration window"""
        try:
            # Import and run config GUI directly (for executable compatibility)
            import threading
            from config_gui import ProxyConfigGUI
            
            def run_config():
                try:
                    app = ProxyConfigGUI()
                    app.root.mainloop()
                except Exception as e:
                    print(f"Config GUI error: {e}")
                    if self.icon:
                        self.icon.notify(f"Config error: {e}", "Uni-Proxy Manager")
            
            # Run in separate thread to not block system tray
            config_thread = threading.Thread(target=run_config, daemon=True)
            config_thread.start()
            
        except Exception as e:
            if self.icon:
                self.icon.notify(f"Failed to open config: {e}", "Uni-Proxy Manager")
    
    def reload_config(self):
        """Reload configuration from file"""
        self.config = self.load_config()
        self.proxy_server = f"{self.config['proxy_server']}:{self.config['proxy_port']}"
        self.proxy_url = f"http://{self.proxy_server}"
        if self.icon:
            self.icon.notify("🔄 Configuration reloaded", f"Uni-Proxy Manager v{self.VERSION}")
    
    def create_menu(self):
        """Create system tray menu"""
        return pystray.Menu(
            pystray.MenuItem("Toggle Proxy", self.toggle_proxy),
            pystray.MenuItem("Check Status", self.check_status),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Enable Proxy", self.enable_proxy),
            pystray.MenuItem("Disable Proxy", self.disable_proxy),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Configuration", self.open_config),
            pystray.MenuItem("Reload Config", self.reload_config),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.quit_app)
        )
    
    def run(self):
        """Run the system tray application"""
        # Create initial icon
        color = (0, 255, 0) if self.is_proxy_enabled else (255, 0, 0)
        icon_image = self.create_icon_image(color)
        
        # Create system tray icon
        self.icon = pystray.Icon(
            "Uni-Proxy Manager",
            icon_image,
            f"Uni-Proxy Manager v{self.VERSION} - Click to toggle",
            menu=self.create_menu()
        )
        
        # Set click action to toggle proxy
        self.icon.default_action = self.toggle_proxy
        
        # Run the icon
        self.icon.run()

def add_to_startup():
    """Add application to Windows startup using silent launcher"""
    try:
        # Get current directory and create path to silent launcher
        script_dir = os.path.dirname(os.path.abspath(__file__))
        silent_launcher = os.path.join(script_dir, "proxy_manager_silent.pyw")
        
        # Create startup shortcut to silent launcher
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           r"Software\Microsoft\Windows\CurrentVersion\Run", 
                           0, winreg.KEY_SET_VALUE)
        
        winreg.SetValueEx(key, "UniProxyManager", 0, winreg.REG_SZ, 
                         f'pythonw "{silent_launcher}"')
        winreg.CloseKey(key)
        
        print("Added to startup successfully (silent mode)!")
        return True
    except Exception as e:
        print(f"Error adding to startup: {e}")
        return False

def remove_from_startup():
    """Remove application from Windows startup"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           r"Software\Microsoft\Windows\CurrentVersion\Run", 
                           0, winreg.KEY_SET_VALUE)
        
        winreg.DeleteValue(key, "UniProxyManager")
        winreg.CloseKey(key)
        
        print("Removed from startup successfully!")
        return True
    except Exception as e:
        print(f"Error removing from startup: {e}")
        return False

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--add-startup":
            add_to_startup()
            sys.exit(0)
        elif sys.argv[1] == "--remove-startup":
            remove_from_startup()
            sys.exit(0)
        elif sys.argv[1] == "--config":
            # Run only the configuration GUI
            from config_gui import ProxyConfigGUI
            app = ProxyConfigGUI()
            app.root.mainloop()
            sys.exit(0)
        elif sys.argv[1] == "--help":
            print(f"Uni-Proxy Manager v{ProxyManager.VERSION}")
            print("Bug fixes: npm error handling, modern UI, round icons")
            print("Usage:")
            print("  python proxy_manager.py           - Run the application")
            print("  python proxy_manager.py --add-startup    - Add to Windows startup")
            print("  python proxy_manager.py --remove-startup - Remove from Windows startup")
            print("  python proxy_manager.py --config         - Open configuration window only")
            print("  python proxy_manager.py --help           - Show this help")
            sys.exit(0)
    
    # Run the proxy manager
    manager = ProxyManager()
    manager.run()
