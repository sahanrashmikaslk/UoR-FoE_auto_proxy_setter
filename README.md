# Uni-Proxy Manager for Windows v1.1.1

A comprehensive proxy management tool for Windows that allows you to easily toggle proxy settings for your entire system, Git, npm, and VS Code from a convenient system tray icon.

## What's New in v1.1.1

- **Modern Dark Theme**: Complete dark theme makeover for the configuration GUI
  - Professional dark color palette with high contrast
  - Enhanced button visibility with proper styling
  - Better spacing and layout for improved usability
- **Silent Operation**: Application now runs completely in background
  - No console window appearing on startup
  - Professional Windows application behavior
  - Silent startup with Windows boot
- **Enhanced Notifications**: Improved system tray notifications
  - Correct version display in notifications
  - Better status feedback with emoji indicators
  - Professional notification styling

## Previous Updates (v1.1)

- **Fixed npm error handling**: No more errors when npm is not installed
- **Modern round icons**: Beautiful circular system tray icons with clear indicators
- **Improved UI**: Modern configuration window with better styling
- **Better error handling**: Graceful handling of missing applications

## Overview

This application provides complete proxy management for Windows environments, specifically designed for switching between university/corporate networks and personal connections. It manages proxy settings across multiple applications and services through a simple system tray interface.

## Features

- **System Tray Integration**: Easy access from the Windows system tray with visual status indicators
- **Comprehensive Proxy Management**:
  - Windows OS system-wide proxy settings
  - Git global proxy configuration
  - npm proxy configuration
  - VS Code proxy settings
- **Auto Startup**: Automatically starts with Windows
- **Visual Indicators**: Red icon (proxy OFF) / Green icon (proxy ON)
- **One-Click Toggle**: Simply click the tray icon to toggle proxy on/off
- **Configuration GUI**: Easy setup and customization interface
- **Command Line Support**: Full CLI interface for advanced users

## System Requirements

- **Operating System**: Windows 10/11
- **Python**: 3.7 or higher
- **RAM**: 50MB
- **Storage**: 10MB
- **Network**: Access to proxy server
- **Dependencies**: pystray, Pillow, psutil

## Installation

### Automatic Installation (Recommended)

1. Download or clone this repository
2. Run `install.bat` as administrator (recommended)
3. The installer will:
   - Check Python installation
   - Install required packages
   - Create default configuration
   - Add application to Windows startup
   - Start the application

### Manual Installation

1. Install Python packages:

   ```cmd
   pip install pystray Pillow psutil
   ```

2. Create default configuration:

   ```cmd
   python -c "import json; json.dump({'proxy_server':'10.50.225.222','proxy_port':'3128','auto_start':True,'enable_windows':True,'enable_git':True,'enable_npm':True,'enable_vscode':True}, open('proxy_config.json','w'), indent=4)"
   ```

3. Add to startup:

   ```cmd
   python proxy_manager.py --add-startup
   ```

4. Start application:
   ```cmd
   python proxy_manager.py
   ```

## File Structure

### Core Application Files (4 files)

- `proxy_manager.py` - Main system tray application
- `proxy_manager_silent.pyw` - Silent launcher (no console window)
- `config_gui.py` - Configuration window interface with dark theme
- `proxy_config.json` - Application settings file

### Installation & Management Scripts (5 files)

- `install.bat` - Complete installation and setup
- `start.bat` - Quick start with automatic silent launch
- `config.bat` - Open configuration window
- `status.bat` - Check current proxy status
- `uninstall.bat` - Remove from Windows startup

### Support Files (3 files)

- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore patterns
- `README.md` - This documentation file

**Total: 12 essential files (clean and organized)**

## Quick Start

1. **Install**: Run `install.bat` as administrator
2. **Start**: Run `start.bat` or look for system tray icon
3. **Configure**: Run `config.bat` to customize settings
4. **Status**: Run `status.bat` to check current state
5. **Remove**: Run `uninstall.bat` to remove from startup

## Usage Guide

### System Tray Icon

After installation, look for a red or green circle icon in your Windows system tray (bottom-right corner, near the clock):

- **Red Circle**: Proxy is currently disabled
- **Green Circle**: Proxy is currently enabled

### Basic Operations

- **Left Click**: Toggle proxy on/off instantly
- **Right Click**: Access full context menu

### Context Menu Options

- **Toggle Proxy**: Switch proxy state on/off
- **Check Status**: Display current proxy status notification
- **Enable Proxy**: Force enable proxy for all configured applications
- **Disable Proxy**: Force disable proxy for all configured applications
- **Configuration**: Open settings window
- **Reload Config**: Refresh configuration from file
- **Quit**: Exit the application

### Configuration Window

Access via right-click menu or run `config.bat`:

- **Proxy Server**: Change proxy server address
- **Port**: Change proxy port number
- **Auto Start**: Enable/disable starting with Windows
- **Target Applications**: Choose which applications to manage
- **Test Connection**: Verify proxy server connectivity

## What Gets Configured

### Windows System Proxy

- Sets system-wide proxy in Internet Settings
- Affects all Windows applications including browsers, Windows Store, etc.
- Includes bypass rules for local network addresses
- Registry location: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings`

### Git Configuration

When enabled:

```bash
git config --global http.proxy http://10.50.225.222:3128
git config --global https.proxy http://10.50.225.222:3128
```

When disabled:

```bash
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### npm Configuration

When enabled:

```bash
npm config set proxy http://10.50.225.222:3128
npm config set https-proxy http://10.50.225.222:3128
```

When disabled:

```bash
npm config delete proxy
npm config delete https-proxy
```

### VS Code Settings

Updates `%APPDATA%\Code\User\settings.json`:

When enabled:

```json
{
  "http.proxy": "http://10.50.225.222:3128",
  "http.proxyStrictSSL": false
}
```

When disabled: Removes proxy settings from configuration.

## Command Line Interface

```cmd
# Run the application
python proxy_manager.py

# Add to Windows startup
python proxy_manager.py --add-startup

# Remove from Windows startup
python proxy_manager.py --remove-startup

# Show help information
python proxy_manager.py --help
```

## Configuration File Format

The `proxy_config.json` file stores all application settings:

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

### Configuration Options

- `proxy_server`: Proxy server IP address or hostname
- `proxy_port`: Proxy server port number
- `auto_start`: Start application with Windows
- `enable_windows`: Manage Windows system proxy
- `enable_git`: Manage Git proxy configuration
- `enable_npm`: Manage npm proxy configuration
- `enable_vscode`: Manage VS Code proxy settings

## Available Batch Commands

- `install.bat` - Full installation and setup
- `config.bat` - Open configuration window
- `run.bat` - Start application manually
- `status.bat` - Check system status and configuration
- `start.bat` - Quick start with setup check
- `uninstall.bat` - Remove from startup

## Troubleshooting

### Application Won't Start

1. Check Python installation:

   ```cmd
   python --version
   ```

2. Verify dependencies:

   ```cmd
   pip list | findstr "pystray"
   ```

3. Run system status check:
   ```cmd
   status.bat
   ```

### System Tray Icon Not Visible

1. Check Windows system tray settings
2. Look in "hidden icons" area (click the up arrow in system tray)
3. Verify application is running in Task Manager
4. Try restarting the application

### Proxy Settings Not Applied

1. Check if application is running (look for tray icon)
2. Verify proxy settings in configuration window
3. Test proxy connection using configuration window
4. Restart affected applications (browsers, VS Code, etc.)
5. Check Windows firewall and antivirus settings

### Startup Issues

1. Check startup registration:

   ```cmd
   reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "UniProxyManager"
   ```

2. Re-add to startup:
   ```cmd
   python proxy_manager.py --add-startup
   ```

## Testing and Verification

### Quick System Test

Use the status checker to verify functionality:

```cmd
status.bat
```

### Manual Testing

Test proxy toggle functionality:

```cmd
# Start the application
start.bat

# Check current status
status.bat

# Configure settings
config.bat
```

### Manual Verification

1. **Windows Proxy**: Check Internet Options > Connections > LAN settings
2. **Git Proxy**: Run `git config --global --get http.proxy`
3. **npm Proxy**: Run `npm config get proxy`
4. **VS Code**: Check File > Preferences > Settings > Application > Proxy

### Status Check

```cmd
status.bat
```

This will check:

- Python installation
- Required packages
- Configuration file
- Current proxy settings for all applications
- Startup registration

## Advanced Usage

### Custom Proxy Configuration

1. Open configuration window: `config.bat`
2. Modify server and port settings
3. Select target applications
4. Test connection
5. Save settings
6. Restart application if needed

### Backup and Restore

**Backup Configuration**:

```cmd
copy proxy_config.json proxy_config_backup.json
```

**Restore Configuration**:

```cmd
copy proxy_config_backup.json proxy_config.json
```

### Multiple Proxy Profiles

Create multiple configuration files and swap them as needed:

```cmd
# Save current config
copy proxy_config.json proxy_config_university.json

# Create home config
echo {"proxy_server":"","proxy_port":"","auto_start":true,"enable_windows":false,"enable_git":false,"enable_npm":false,"enable_vscode":false} > proxy_config_home.json

# Switch profiles
copy proxy_config_university.json proxy_config.json
```

## Security Considerations

- Application only modifies local proxy settings
- No external data transmission except through configured proxy
- Configuration stored locally in JSON format
- No administrative privileges required for normal operation
- Registry modifications limited to current user scope

## Default Configuration

Pre-configured for University of Roehampton:

- **Server**: 10.50.225.222
- **Port**: 3128
- **Protocol**: HTTP
- **Applications**: Windows, Git, npm, VS Code

## Uninstallation

### Remove from Startup

```cmd
uninstall.bat
```

### Complete Removal

1. Run `uninstall.bat` to remove from startup
2. Close the application (right-click tray icon > Quit)
3. Delete the application folder

### Manual Cleanup

```cmd
# Remove startup entry
python proxy_manager.py --remove-startup

# Or manually remove registry entry
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "UniProxyManager"
```

## Support and Debugging

### Log Information

The application provides console output when run from command line. For debugging:

```cmd
python proxy_manager.py
```

### Common Error Messages

- **"Python not found"**: Install Python and add to PATH
- **"Access denied"**: Run as administrator or check permissions
- **"Proxy unreachable"**: Verify network connection and proxy server
- **"Settings not applying"**: Restart affected applications

### Getting Help

1. Run `python proxy_manager.py --help` for command line options
2. Use `status.bat` for system diagnostics
3. Check configuration with `config.bat`

For technical support regarding proxy server settings, contact your network administrator or IT department.

## Version History

### Version 1.1.1 (August 25, 2025)

- **Modern Dark Theme**: Complete UI overhaul with professional dark theme
- **Silent Operation**: Application runs without console window
- **Enhanced Button Visibility**: Fixed GUI button visibility issues
- **Better Notifications**: Improved system tray notifications with correct version display
- **Larger Window**: Increased configuration window size for better usability

### Version 1.1 (August 25, 2025)

- **Fixed npm error handling**: Graceful handling when npm is not installed
- **Modern round icons**: Circular system tray icons with better visual indicators
- **Improved configuration GUI**: Better styling and layout
- **Enhanced error handling**: Better error reporting and user feedback
- **Updated branding**: Renamed to "Uni-Proxy Manager" throughout

### Version 1.0 (Initial Release)

- System tray integration for easy proxy toggling
- Windows system proxy management
- Git, npm, and VS Code proxy configuration
- Auto-startup with Windows
- Configuration GUI and command line interface

## License

This project is open source and available under the MIT License.
