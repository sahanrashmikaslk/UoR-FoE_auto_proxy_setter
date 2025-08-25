# Proxy Manager for Windows

A comprehensive proxy management tool for Windows that allows you to easily toggle proxy settings for your entire system, Git, npm, and VS Code from a convenient system tray icon.

## Features

- **System Tray Integration**: Easy access from the Windows system tray
- **Comprehensive Proxy Management**: 
  - Windows OS proxy settings
  - Git proxy configuration
  - npm proxy configuration
  - VS Code proxy settings
- **Auto Startup**: Starts automatically with Windows
- **Visual Indicators**: Green icon (proxy ON) / Red icon (proxy OFF)
- **One-Click Toggle**: Simply click the tray icon to toggle proxy on/off

## Installation

1. Make sure Python 3.7+ is installed on your system
2. Double-click `install.bat` to install and set up the application
3. The application will be added to Windows startup automatically

## Usage

### System Tray Icon
- **Green Icon**: Proxy is enabled
- **Red Icon**: Proxy is disabled
- **Left Click**: Toggle proxy on/off
- **Right Click**: Access menu with more options

### Menu Options
- **Toggle Proxy**: Switch proxy on/off
- **Check Status**: Show current proxy status
- **Enable Proxy**: Force enable proxy
- **Disable Proxy**: Force disable proxy
- **Quit**: Exit the application

### Manual Control
You can also run the application manually:
- `run.bat` - Start the proxy manager
- `uninstall.bat` - Remove from startup

### Command Line Options
```bash
python proxy_manager.py                    # Run the application
python proxy_manager.py --add-startup      # Add to Windows startup
python proxy_manager.py --remove-startup   # Remove from Windows startup
python proxy_manager.py --help             # Show help
```

## Proxy Configuration

The application is pre-configured with the University of Roehampton proxy settings:
- **Proxy Server**: 10.50.225.222:3128
- **Protocol**: HTTP

## What Gets Configured

When you enable the proxy, the application configures:

1. **Windows System Proxy**: Internet settings for all Windows applications
2. **Git Configuration**: 
   - `git config --global http.proxy`
   - `git config --global https.proxy`
3. **npm Configuration**:
   - `npm config set proxy`
   - `npm config set https-proxy`
4. **VS Code Settings**: Updates `settings.json` with proxy configuration

## Requirements

- Windows 10/11
- Python 3.7+
- pip (Python package manager)

## Dependencies

- `pystray` - System tray functionality
- `Pillow` - Icon generation
- `psutil` - System utilities

## Troubleshooting

### Application won't start
- Make sure Python is installed and in your PATH
- Run `install.bat` as administrator if needed
- Check that all requirements are installed: `pip install -r requirements.txt`

### Proxy not working for specific applications
- Some applications may need to be restarted after changing proxy settings
- Corporate firewalls might block certain proxy configurations
- Try disabling and re-enabling the proxy

### Icon not appearing in system tray
- Check if the application is running in Task Manager
- Make sure system tray icons are not hidden in Windows settings

## Customization

To change the proxy server, edit the `proxy_server` variable in `proxy_manager.py`:

```python
self.proxy_server = "your.proxy.server:port"
```

## License

This project is open source and available under the MIT License.
