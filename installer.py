"""
Uni-Proxy Manager - Single File Installer
Creates a complete installation with embedded executable and setup
"""

import os
import sys
import subprocess
import json
import shutil
import tempfile
import winreg
from pathlib import Path
import base64
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class UniProxyInstaller:
    def __init__(self):
        self.version = "1.1.1"
        self.app_name = "Uni-Proxy Manager"
        self.install_path = Path("C:/Program Files/UniProxyManager")
        self.portable_mode = False
        
    def show_installer_gui(self):
        """Show installation GUI"""
        root = tk.Tk()
        root.title(f"{self.app_name} v{self.version} - Installer")
        root.geometry("900x800")  # Even larger: increased from 800x700
        root.minsize(850, 750)     # Higher minimum size 
        root.resizable(True, True)  # Allow resizing
        
        # Center the window on screen
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (900 // 2)
        y = (root.winfo_screenheight() // 2) - (800 // 2)
        root.geometry(f"900x800+{x}+{y}")
        
        # Configure style with better button visibility
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles for better visibility
        style.configure('Install.TButton', 
                       font=('Arial', 12, 'bold'),  # Larger font
                       foreground='white',
                       background='#0078d4',
                       focuscolor='none',
                       padding=(25, 15))  # Bigger padding
        style.map('Install.TButton',
                 background=[('active', '#106ebe'), ('pressed', '#005a9e')])
        
        style.configure('Cancel.TButton',
                       font=('Arial', 11),  # Larger font
                       padding=(20, 12))  # Bigger padding
        
        # Main frame with more padding
        main_frame = ttk.Frame(root, padding="40")  # Increased from 30
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title with larger font
        title_label = ttk.Label(main_frame, text=f"{self.app_name} v{self.version}", 
                               font=("Arial", 20, "bold"))  # Increased from 18
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))  # More spacing
        
        # Description with better formatting
        desc_text = """Complete Windows proxy management solution.
        
✅ System tray integration with one-click toggle
✅ Manages Windows, Git, npm, and VS Code proxy settings  
✅ Auto-startup with Windows option
✅ Modern dark theme configuration interface
✅ Silent background operation"""
        
        desc_label = ttk.Label(main_frame, text=desc_text, justify=tk.LEFT,
                              font=("Arial", 11))  # Slightly larger font
        desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 30), sticky=tk.W)  # More spacing
        
        # Installation options with better spacing
        options_frame = ttk.LabelFrame(main_frame, text="Installation Options", 
                                      padding="20", style="Options.TLabelframe")  # More padding
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 30))  # More spacing
        
        # Installation type with better spacing
        self.install_type = tk.StringVar(value="standard")
        
        # Standard installation option
        std_radio = ttk.Radiobutton(options_frame, text="Standard Installation (Recommended)", 
                                   variable=self.install_type, value="standard",
                                   style="Option.TRadiobutton")
        std_radio.grid(row=0, column=0, sticky=tk.W, pady=(5, 8))
        
        ttk.Label(options_frame, text="   • Installs to Program Files", 
                 foreground="gray", font=("Arial", 9)).grid(row=1, column=0, sticky=tk.W, padx=25, pady=2)
        ttk.Label(options_frame, text="   • Auto-startup with Windows", 
                 foreground="gray", font=("Arial", 9)).grid(row=2, column=0, sticky=tk.W, padx=25, pady=2)
        ttk.Label(options_frame, text="   • Creates Start Menu shortcuts", 
                 foreground="gray", font=("Arial", 9)).grid(row=3, column=0, sticky=tk.W, padx=25, pady=2)
        
        # Portable installation option
        port_radio = ttk.Radiobutton(options_frame, text="Portable Installation", 
                                    variable=self.install_type, value="portable",
                                    style="Option.TRadiobutton")
        port_radio.grid(row=4, column=0, sticky=tk.W, pady=(20, 8))
        
        ttk.Label(options_frame, text="   • Install to custom folder", 
                 foreground="gray", font=("Arial", 9)).grid(row=5, column=0, sticky=tk.W, padx=25, pady=2)
        ttk.Label(options_frame, text="   • No system integration", 
                 foreground="gray", font=("Arial", 9)).grid(row=6, column=0, sticky=tk.W, padx=25, pady=2)
        ttk.Label(options_frame, text="   • Easily removable", 
                 foreground="gray", font=("Arial", 9)).grid(row=7, column=0, sticky=tk.W, padx=25, pady=(2, 5))
        
        # Installation path with better layout
        path_frame = ttk.LabelFrame(main_frame, text="Installation Location", padding="20")  # More padding
        path_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 30))  # More spacing
        
        ttk.Label(path_frame, text="Path:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))  # Larger font
        self.path_var = tk.StringVar(value=str(self.install_path))
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=60, font=("Arial", 11))  # Larger font
        path_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 15))
        
        browse_btn = ttk.Button(path_frame, text="Browse...", 
                               command=self.browse_install_path,
                               style="Cancel.TButton")
        browse_btn.grid(row=1, column=1)
        
        path_frame.columnconfigure(0, weight=1)
        
        # Proxy configuration with better layout
        proxy_frame = ttk.LabelFrame(main_frame, text="Proxy Configuration", padding="20")  # More padding
        proxy_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 30))  # More spacing
        
        ttk.Label(proxy_frame, text="Server:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))  # Larger font
        self.proxy_server = tk.StringVar(value="10.50.225.222")
        server_entry = ttk.Entry(proxy_frame, textvariable=self.proxy_server, width=25, font=("Arial", 11))  # Larger font
        server_entry.grid(row=0, column=1, sticky=tk.W, pady=(0, 15))  # More spacing
        
        ttk.Label(proxy_frame, text="Port:", font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W, padx=(0, 10))  # Larger font
        self.proxy_port = tk.StringVar(value="3128")
        port_entry = ttk.Entry(proxy_frame, textvariable=self.proxy_port, width=25, font=("Arial", 11))  # Larger font
        port_entry.grid(row=1, column=1, sticky=tk.W)
        
        # Buttons (much larger and more visible)
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(40, 30), sticky=(tk.W, tk.E))  # More spacing
        
        # Create button container for better centering
        button_container = ttk.Frame(button_frame)
        button_container.pack(expand=True)
        
        # Install button with custom style - much larger
        install_btn = ttk.Button(button_container, text="Install Now", 
                                command=self.start_installation, 
                                style="Install.TButton")
        install_btn.pack(side=tk.LEFT, padx=(0, 20))  # More spacing between buttons
        
        # Cancel button - larger
        cancel_btn = ttk.Button(button_container, text="Cancel", 
                               command=root.quit,
                               style="Cancel.TButton")
        cancel_btn.pack(side=tk.LEFT)
        
        # Add more space at bottom
        spacer_frame = ttk.Frame(main_frame)
        spacer_frame.grid(row=6, column=0, columnspan=2, pady=(0, 30))  # More bottom space
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Update path when installation type changes
        def update_path(*args):
            if self.install_type.get() == "standard":
                self.path_var.set("C:/Program Files/UniProxyManager")
            else:
                self.path_var.set(str(Path.home() / "Desktop" / "UniProxyManager"))
        
        self.install_type.trace('w', update_path)
        
        root.mainloop()
    
    def is_admin(self):
        """Check if running with administrator privileges"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def restart_as_admin(self):
        """Restart the application with administrator privileges"""
        try:
            import ctypes
            import sys
            
            # Get the current executable path
            if getattr(sys, 'frozen', False):
                # Running as executable
                script = sys.executable
            else:
                # Running as Python script
                script = sys.argv[0]
            
            # Restart with admin privileges
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", script, "", "", 1
            )
            
            # Close current instance
            sys.exit(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restart as administrator: {e}")
    
    def browse_install_path(self):
        """Browse for installation path"""
        path = filedialog.askdirectory(title="Select Installation Directory")
        if path:
            self.path_var.set(path)
    
    def start_installation(self):
        """Start the installation process"""
        try:
            install_path = Path(self.path_var.get()) / "UniProxyManager"
            is_standard = self.install_type.get() == "standard"
            
            # Check for admin rights if installing to Program Files
            if is_standard and "Program Files" in str(install_path):
                if not self.is_admin():
                    result = messagebox.askyesno("Administrator Required", 
                                               """This installation requires administrator privileges to install to Program Files.

Click 'Yes' to restart as administrator, or 'No' to choose a different location.""")
                    if result:
                        self.restart_as_admin()
                        return
                    else:
                        # Let user choose different path
                        messagebox.showinfo("Choose Different Location", 
                                          "Please select a different installation location or choose Portable Installation.")
                        return
            
            # Create progress window
            progress_window = tk.Toplevel()
            progress_window.title("Installing...")
            progress_window.geometry("500x250")  # Larger progress window
            progress_window.resizable(False, False)
            progress_window.grab_set()
            
            # Center the progress window
            progress_window.update_idletasks()
            x = (progress_window.winfo_screenwidth() // 2) - (500 // 2)
            y = (progress_window.winfo_screenheight() // 2) - (250 // 2)
            progress_window.geometry(f"500x250+{x}+{y}")
            
            ttk.Label(progress_window, text="Installing Uni-Proxy Manager...", 
                     font=("Arial", 14, "bold")).pack(pady=30)  # Larger font
            
            progress = ttk.Progressbar(progress_window, length=400, mode='indeterminate')  # Wider progress bar
            progress.pack(pady=15)
            progress.start()
            
            status_label = ttk.Label(progress_window, text="Preparing installation...",
                                   font=("Arial", 11))  # Larger font
            status_label.pack(pady=15)
            
            # Update function
            def update_status(text):
                status_label.config(text=text)
                progress_window.update()
            
            # Perform installation with better error handling
            try:
                success = self.perform_installation(install_path, is_standard, update_status)
            except PermissionError as e:
                progress.stop()
                progress_window.destroy()
                messagebox.showerror("Permission Error", 
                                   f"""Installation failed due to insufficient permissions.

Error: {e}

Try one of these solutions:
1. Run as Administrator (right-click → Run as administrator)
2. Choose a different installation location (like Desktop)
3. Use Portable Installation instead""")
                return
            except Exception as e:
                progress.stop()
                progress_window.destroy()
                messagebox.showerror("Installation Error", 
                                   f"""Installation failed with error:

{e}

Please try:
1. Choosing a different installation location
2. Running as Administrator
3. Checking available disk space""")
                return
            
            progress.stop()
            progress_window.destroy()
            
            if success:
                messagebox.showinfo("Installation Complete", 
                                  f"""✅ {self.app_name} has been successfully installed!

📍 Location: {install_path}

🚀 The application is now running in your system tray.
Look for the red/green circle icon to toggle proxy settings.

{"✅ Auto-startup has been enabled." if is_standard else "💡 You can enable auto-startup from the configuration menu."}""")
                
                # Start the application
                if install_path.exists():
                    exe_path = install_path / "UniProxyManager.exe"
                    if exe_path.exists():
                        subprocess.Popen([str(exe_path)], cwd=str(install_path))
                
                sys.exit(0)
            else:
                messagebox.showerror("Installation Failed", 
                                   "Installation failed. Please check permissions and try again.")
                
        except Exception as e:
            messagebox.showerror("Installation Error", f"Installation failed: {e}")
    
    def perform_installation(self, install_path, is_standard, update_status):
        """Perform the actual installation"""
        try:
            update_status("Creating installation directory...")
            
            # Create installation directory
            install_path.mkdir(parents=True, exist_ok=True)
            
            update_status("Extracting application files...")
            
            # Get the directory where this installer is located
            installer_dir = Path(__file__).parent
            
            # Copy executable and required files
            files_to_copy = [
                "UniProxyManager.exe",
                "proxy_config.json",
                "README.md"
            ]
            
            # Check if we have the files in current directory or dist
            source_dirs = [installer_dir, installer_dir / "dist", installer_dir / "UniProxyManager_Portable"]
            
            for file_name in files_to_copy:
                copied = False
                for source_dir in source_dirs:
                    source_file = source_dir / file_name
                    if source_file.exists():
                        dest_file = install_path / file_name
                        shutil.copy2(source_file, dest_file)
                        copied = True
                        break
                
                if not copied and file_name == "UniProxyManager.exe":
                    raise Exception(f"Required file {file_name} not found!")
            
            update_status("Creating configuration...")
            
            # Create configuration file with user settings
            config = {
                "proxy_server": self.proxy_server.get(),
                "proxy_port": self.proxy_port.get(),
                "auto_start": is_standard,
                "enable_windows": True,
                "enable_git": True,
                "enable_npm": True,
                "enable_vscode": True
            }
            
            config_file = install_path / "proxy_config.json"
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            
            if is_standard:
                update_status("Setting up Windows integration...")
                
                # Add to Windows startup
                try:
                    exe_path = install_path / "UniProxyManager.exe"
                    startup_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                                r"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 
                                                0, winreg.KEY_SET_VALUE)
                    winreg.SetValueEx(startup_key, "UniProxyManager", 0, winreg.REG_SZ, str(exe_path))
                    winreg.CloseKey(startup_key)
                except Exception as e:
                    print(f"Failed to add to startup: {e}")
                
                # Create Start Menu shortcut (optional)
                try:
                    update_status("Creating shortcuts...")
                    start_menu = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
                    shortcut_dir = start_menu / "Uni-Proxy Manager"
                    shortcut_dir.mkdir(exist_ok=True)
                    
                    # Create batch file as shortcut
                    shortcut_file = shortcut_dir / "Uni-Proxy Manager.bat"
                    with open(shortcut_file, 'w') as f:
                        f.write(f'@echo off\nstart "" "{install_path / "UniProxyManager.exe"}"\n')
                    
                    # Create uninstall shortcut
                    uninstall_file = shortcut_dir / "Uninstall.bat"
                    with open(uninstall_file, 'w') as f:
                        f.write(f'''@echo off
echo Removing Uni-Proxy Manager...
reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "UniProxyManager" /f 2>nul
rmdir /s /q "{install_path}"
rmdir /s /q "{shortcut_dir}"
echo Uninstallation complete!
pause
''')
                except Exception as e:
                    print(f"Failed to create shortcuts: {e}")
            
            update_status("Installation complete!")
            return True
            
        except Exception as e:
            print(f"Installation error: {e}")
            return False

def main():
    """Main installer entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print(f"""
Uni-Proxy Manager v1.1.1 - Single File Installer

This installer creates a complete installation of Uni-Proxy Manager
including the executable, configuration, and Windows integration.

Options:
  --help     Show this help message
  --silent   Silent installation (uses defaults)

For GUI installation, just run without arguments.
        """)
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == "--silent":
        # Silent installation with defaults
        installer = UniProxyInstaller()
        install_path = Path("C:/Program Files/UniProxyManager")
        
        def dummy_update(text):
            print(f"[INSTALL] {text}")
        
        success = installer.perform_installation(install_path, True, dummy_update)
        if success:
            print("✅ Installation completed successfully!")
            # Start the application
            exe_path = install_path / "UniProxyManager.exe"
            if exe_path.exists():
                subprocess.Popen([str(exe_path)], cwd=str(install_path))
        else:
            print("❌ Installation failed!")
            sys.exit(1)
    else:
        # GUI installation
        installer = UniProxyInstaller()
        installer.show_installer_gui()

if __name__ == "__main__":
    main()
