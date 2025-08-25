# Proxy Manager for Windows - Complete Setup Guide

## 🎯 What This Application Does

This is a comprehensive proxy management tool that provides:

- **System Tray Integration**: Easy toggle from Windows system tray
- **Complete Proxy Control**: Manages Windows OS, Git, npm, and VS Code proxy settings
- **Auto Startup**: Starts automatically with Windows
- **Visual Indicators**: Green icon (ON) / Red icon (OFF)
- **One-Click Toggle**: Simply click the tray icon to toggle proxy

## 🚀 Quick Start

1. **Install**: Double-click `install.bat`
2. **Configure**: Use `config.bat` to customize settings (optional)
3. **Use**: Look for the red/green proxy icon in your system tray

## 📁 Files Overview

### Main Files
- `proxy_manager.py` - Main application (system tray)
- `config_gui.py` - Configuration window
- `proxy_config.json` - Settings file

### Batch Files
- `install.bat` - Complete installation
- `start.bat` - Quick start/setup check
- `run.bat` - Start application manually
- `config.bat` - Open configuration
- `status.bat` - Check system status
- `uninstall.bat` - Remove from startup

### Support Files
- `requirements.txt` - Python dependencies
- `test_proxy.py` - Test functionality
- `README.md` - Documentation

## 🛠 Installation Steps

### Automatic Installation
```cmd
# Run as administrator (recommended)
install.bat
```

### Manual Installation
```cmd
# 1. Install Python packages
pip install pystray Pillow psutil

# 2. Create default config
python -c "import json; json.dump({'proxy_server':'10.50.225.222','proxy_port':'3128','auto_start':True,'enable_windows':True,'enable_git':True,'enable_npm':True,'enable_vscode':True}, open('proxy_config.json','w'), indent=4)"

# 3. Add to startup
python proxy_manager.py --add-startup

# 4. Start application
python proxy_manager.py
```

## 🎮 Usage Guide

### System Tray Icon
- **Green Circle**: Proxy is enabled
- **Red Circle**: Proxy is disabled
- **Left Click**: Toggle proxy on/off
- **Right Click**: Access full menu

### Menu Options
- **Toggle Proxy**: Switch proxy on/off
- **Check Status**: Show current status
- **Enable/Disable Proxy**: Force specific state
- **Configuration**: Open settings window
- **Reload Config**: Refresh settings
- **Quit**: Exit application

### Configuration Window
- **Proxy Server**: Change proxy server address
- **Port**: Change proxy port
- **Auto Start**: Start with Windows
- **Target Applications**: Choose which apps to configure

## 🔧 What Gets Configured

### Windows System Proxy
- Sets system-wide proxy in Internet Settings
- Affects browsers, Windows Store, etc.
- Includes bypass rules for local addresses

### Git Configuration
```bash
git config --global http.proxy http://10.50.225.222:3128
git config --global https.proxy http://10.50.225.222:3128
```

### npm Configuration
```bash
npm config set proxy http://10.50.225.222:3128
npm config set https-proxy http://10.50.225.222:3128
```

### VS Code Settings
Adds to `%APPDATA%\Code\User\settings.json`:
```json
{
    "http.proxy": "http://10.50.225.222:3128",
    "http.proxyStrictSSL": false
}
```

## 🔍 Troubleshooting

### Application Won't Start
```cmd
# Check Python installation
python --version

# Check dependencies
pip list | findstr "pystray\|Pillow\|psutil"

# Run status check
status.bat
```

### Proxy Not Working
1. Check if application is running (look for tray icon)
2. Verify proxy settings in configuration
3. Test proxy connection in config window
4. Restart affected applications

### Icon Not Visible
- Check Windows system tray settings
- Look in "hidden icons" area
- Try restarting the application

### Startup Issues
```cmd
# Check startup registration
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "ProxyManager"

# Re-add to startup
python proxy_manager.py --add-startup
```

## 🎯 Advanced Usage

### Custom Proxy Settings
1. Run `config.bat`
2. Change server/port as needed
3. Test connection
4. Save settings
5. Restart application

### Command Line Control
```cmd
# Add to startup
python proxy_manager.py --add-startup

# Remove from startup
python proxy_manager.py --remove-startup

# Show help
python proxy_manager.py --help
```

### Backup Configuration
Simply copy `proxy_config.json` to backup your settings.

## 📋 System Requirements

- **OS**: Windows 10/11
- **Python**: 3.7 or higher
- **RAM**: 50MB
- **Storage**: 10MB
- **Network**: Access to proxy server

## 🔒 Security Notes

- Application only modifies local proxy settings
- No data is sent externally except through configured proxy
- Configuration stored locally in JSON format
- No elevation required for normal operation

## 🆘 Support

### Quick Diagnostics
```cmd
# Full system check
status.bat

# Test functionality
python test_proxy.py

# View current settings
type proxy_config.json
```

### Common Issues
1. **Python not found**: Install Python and add to PATH
2. **Access denied**: Run as administrator
3. **Proxy unreachable**: Check network connection
4. **Settings not applying**: Restart affected applications

## 📝 Configuration File Format

```json
{
    "proxy_server": "10.50.225.222",
    "proxy_port": "3128", 
    "auto_start": true,
    "enable_windows": true,
    "enable_git": true,
    "enable_npm": true,
    "enable_vscode": true
}
```

## 🔄 Uninstallation

```cmd
# Remove from startup
uninstall.bat

# Or manually
python proxy_manager.py --remove-startup

# Delete folder to completely remove
```

---

**University of Roehampton Proxy Settings**
- Server: 10.50.225.222
- Port: 3128
- Protocol: HTTP

For technical support, refer to your IT department or system administrator.
