import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from pathlib import Path

class ProxyConfigGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Uni-Proxy Manager v1.1 - Configuration")
        self.root.geometry("800x700")  # Much larger window for visibility
        self.root.minsize(750, 650)    # Prevent shrinking too small
        self.root.resizable(True, True)  # Allow resizing
        
        # Modern dark theme colors
        self.colors = {
            'bg_primary': '#1e1e1e',      # Main background
            'bg_secondary': '#2d2d2d',    # Panel background
            'bg_tertiary': '#3c3c3c',     # Input background
            'text_primary': '#ffffff',    # Main text
            'text_secondary': '#b0b0b0',  # Secondary text
            'accent': '#0d7377',          # Accent color (teal)
            'accent_hover': '#14a085',    # Accent hover
            'border': '#404040',          # Border color
            'success': '#22c55e',         # Success green
            'warning': '#f59e0b',         # Warning orange
            'error': '#ef4444'            # Error red
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Configure modern dark theme
        self.setup_dark_theme()
        
        # Configuration file path
        self.config_file = Path(__file__).parent / "proxy_config.json"
        
        # Load existing configuration
        self.config = self.load_config()
        
        self.create_widgets()
        self.load_values()
        self.center_window()  # Center window after everything is loaded
    
    def center_window(self):
        """Center the window on the screen and ensure it's visible"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = max(0, (self.root.winfo_screenwidth() // 2) - (width // 2))
        y = max(0, (self.root.winfo_screenheight() // 2) - (height // 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        print(f"Window size: {width}x{height} at position {x},{y}")  # Debug info
    
    def setup_dark_theme(self):
        """Setup simplified dark theme focusing on what works"""
        style = ttk.Style()
        
        # Use most compatible theme
        available_themes = style.theme_names()
        if 'winnative' in available_themes:
            style.theme_use('winnative')
        elif 'clam' in available_themes:
            style.theme_use('clam')
        else:
            style.theme_use('default')
        
        # Configure only essential frame styles
        style.configure('Dark.TFrame', 
                       background=self.colors['bg_primary'],
                       relief='flat')
        
        # Configure label frame (panels) with visible borders
        style.configure('Dark.TLabelframe', 
                       background=self.colors['bg_secondary'],
                       borderwidth=2,
                       relief='solid',
                       bordercolor='#606060')
        style.configure('Dark.TLabelframe.Label', 
                       background=self.colors['bg_secondary'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        
        # Configure labels with high contrast
        style.configure('Dark.TLabel', 
                       background=self.colors['bg_secondary'],
                       foreground='white',
                       font=('Segoe UI', 9))
        
        style.configure('Title.TLabel', 
                       background=self.colors['bg_primary'],
                       foreground='#00BFFF',  # Bright blue for visibility
                       font=('Segoe UI', 18, 'bold'))
        
        style.configure('Status.TLabel', 
                       background=self.colors['bg_primary'],
                       foreground='#C0C0C0',
                       font=('Segoe UI', 9, 'italic'))
        
        # Configure entry widgets with high contrast
        style.configure('Dark.TEntry',
                       fieldbackground='white',  # White background for inputs
                       background='white',
                       foreground='black',       # Black text on white
                       bordercolor='#808080',
                       insertcolor='black',
                       font=('Segoe UI', 9))
    
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            "proxy_server": "10.50.225.222",
            "proxy_port": "3128",
            "auto_start": True,
            "enable_windows": True,
            "enable_git": True,
            "enable_npm": True,
            "enable_vscode": True
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_config.update(config)
                    return default_config
            except:
                return default_config
        return default_config
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
            return False
    
    def create_widgets(self):
        """Create modern dark-themed GUI widgets"""
        # Main frame with dark theme
        main_frame = ttk.Frame(self.root, padding="40", style='Dark.TFrame')  # Increased padding
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title label with modern styling
        title_label = ttk.Label(main_frame, text="Uni-Proxy Manager v1.1", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 25))
        
        # Proxy Settings Section
        proxy_frame = ttk.LabelFrame(main_frame, text="  Proxy Settings  ", 
                                   padding="20", style='Dark.TLabelframe')
        proxy_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Server input
        ttk.Label(proxy_frame, text="Proxy Server:", style='Dark.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=(0, 12), padx=(0, 15))
        self.server_var = tk.StringVar()
        server_entry = ttk.Entry(proxy_frame, textvariable=self.server_var, 
                               width=35, style='Dark.TEntry')
        server_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 12))
        
        # Port input
        ttk.Label(proxy_frame, text="Port:", style='Dark.TLabel').grid(
            row=1, column=0, sticky=tk.W, pady=(0, 12), padx=(0, 15))
        self.port_var = tk.StringVar()
        port_entry = ttk.Entry(proxy_frame, textvariable=self.port_var, 
                             width=15, style='Dark.TEntry')
        port_entry.grid(row=1, column=1, sticky=tk.W, pady=(0, 12))
        
        # Application Settings Section
        app_frame = ttk.LabelFrame(main_frame, text="  Application Settings  ", 
                                 padding="20", style='Dark.TLabelframe')
        app_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.auto_start_var = tk.BooleanVar()
        auto_start_cb = tk.Checkbutton(app_frame, text="Start with Windows", 
                                      variable=self.auto_start_var,
                                      bg=self.colors['bg_secondary'],
                                      fg='white',
                                      selectcolor='#32CD32',  # Lime green when checked
                                      activebackground=self.colors['bg_secondary'],
                                      activeforeground='white',
                                      font=('Segoe UI', 9),
                                      indicatoron=True,
                                      relief='flat',
                                      borderwidth=0)
        auto_start_cb.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Proxy Target Settings Section
        target_frame = ttk.LabelFrame(main_frame, text="  Proxy Targets  ", 
                                    padding="20", style='Dark.TLabelframe')
        target_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 25))
        
        self.windows_var = tk.BooleanVar()
        windows_cb = tk.Checkbutton(target_frame, text="Windows System Proxy", 
                                   variable=self.windows_var,
                                   bg=self.colors['bg_secondary'],
                                   fg='white',
                                   selectcolor='#32CD32',  # Lime green when checked
                                   activebackground=self.colors['bg_secondary'],
                                   activeforeground='white',
                                   font=('Segoe UI', 9),
                                   indicatoron=True,
                                   relief='flat',
                                   borderwidth=0)
        windows_cb.grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        
        self.git_var = tk.BooleanVar()
        git_cb = tk.Checkbutton(target_frame, text="Git Configuration", 
                               variable=self.git_var,
                               bg=self.colors['bg_secondary'],
                               fg='white',
                               selectcolor='#32CD32',  # Lime green when checked
                               activebackground=self.colors['bg_secondary'],
                               activeforeground='white',
                               font=('Segoe UI', 9),
                               indicatoron=True,
                               relief='flat',
                               borderwidth=0)
        git_cb.grid(row=1, column=0, sticky=tk.W, pady=(0, 8))
        
        self.npm_var = tk.BooleanVar()
        npm_cb = tk.Checkbutton(target_frame, text="npm Configuration (if available)", 
                               variable=self.npm_var,
                               bg=self.colors['bg_secondary'],
                               fg='white',
                               selectcolor='#32CD32',  # Lime green when checked
                               activebackground=self.colors['bg_secondary'],
                               activeforeground='white',
                               font=('Segoe UI', 9),
                               indicatoron=True,
                               relief='flat',
                               borderwidth=0)
        npm_cb.grid(row=2, column=0, sticky=tk.W, pady=(0, 8))
        
        self.vscode_var = tk.BooleanVar()
        vscode_cb = tk.Checkbutton(target_frame, text="VS Code Settings", 
                                  variable=self.vscode_var,
                                  bg=self.colors['bg_secondary'],
                                  fg='white',
                                  selectcolor='#32CD32',  # Lime green when checked
                                  activebackground=self.colors['bg_secondary'],
                                  activeforeground='white',
                                  font=('Segoe UI', 9),
                                  indicatoron=True,
                                  relief='flat',
                                  borderwidth=0)
        vscode_cb.grid(row=3, column=0, sticky=tk.W, pady=(0, 8))
        
        # Buttons with basic tkinter widgets for maximum visibility
        button_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        button_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(30, 40))
        
        # Configure button frame to expand properly
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        
        # Use basic tkinter Buttons with MAXIMUM VISIBILITY
        save_btn = tk.Button(button_frame, 
                            text="💾 SAVE CONFIGURATION",
                            command=self.save_settings,
                            bg="#228B22",           # Forest green background
                            fg="white",             # White text
                            activebackground="#32CD32",  # Lighter green when pressed
                            activeforeground="white",
                            font=("Segoe UI", 12, "bold"),  # Even larger font
                            relief="raised",
                            borderwidth=5,          # Thicker border
                            padx=30,               # More padding
                            pady=15,
                            cursor="hand2",
                            width=20,              # Fixed width
                            height=2)              # Fixed height
        save_btn.grid(row=0, column=0, padx=15, pady=10, sticky="ew")
        
        test_btn = tk.Button(button_frame,
                            text="🔧 TEST CONNECTION", 
                            command=self.test_connection,
                            bg="#4169E1",           # Royal blue background
                            fg="white",             # White text
                            activebackground="#6495ED",  # Lighter blue when pressed
                            activeforeground="white",
                            font=("Segoe UI", 12, "bold"),  # Even larger font
                            relief="raised",
                            borderwidth=5,          # Thicker border
                            padx=30,               # More padding
                            pady=15,
                            cursor="hand2",
                            width=20,              # Fixed width
                            height=2)              # Fixed height
        test_btn.grid(row=0, column=1, padx=15, pady=10, sticky="ew")
        
        cancel_btn = tk.Button(button_frame,
                              text="❌ CANCEL",
                              command=self.root.quit,
                              bg="#DC143C",          # Crimson red background
                              fg="white",            # White text
                              activebackground="#FF6347",  # Lighter red when pressed
                              activeforeground="white",
                              font=("Segoe UI", 12, "bold"),  # Even larger font
                              relief="raised",
                              borderwidth=5,          # Thicker border
                              padx=30,               # More padding
                              pady=15,
                              cursor="hand2",
                              width=15,              # Fixed width
                              height=2)              # Fixed height
        cancel_btn.grid(row=0, column=2, padx=15, pady=10, sticky="ew")
        
        # Status label at the bottom
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                               style='Status.TLabel')
        status_label.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
        
        # Configure grid weights for proper resizing
        main_frame.columnconfigure(1, weight=1)
        proxy_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def load_values(self):
        """Load configuration values into GUI"""
        self.server_var.set(self.config.get("proxy_server", ""))
        self.port_var.set(self.config.get("proxy_port", ""))
        self.auto_start_var.set(self.config.get("auto_start", True))
        self.windows_var.set(self.config.get("enable_windows", True))
        self.git_var.set(self.config.get("enable_git", True))
        self.npm_var.set(self.config.get("enable_npm", True))
        self.vscode_var.set(self.config.get("enable_vscode", True))
    
    def save_settings(self):
        """Save settings and close"""
        # Validate inputs
        server = self.server_var.get().strip()
        port = self.port_var.get().strip()
        
        if not server:
            messagebox.showerror("Error", "Proxy server cannot be empty")
            return
        
        if not port or not port.isdigit():
            messagebox.showerror("Error", "Port must be a valid number")
            return
        
        # Update configuration
        self.config.update({
            "proxy_server": server,
            "proxy_port": port,
            "auto_start": self.auto_start_var.get(),
            "enable_windows": self.windows_var.get(),
            "enable_git": self.git_var.get(),
            "enable_npm": self.npm_var.get(),
            "enable_vscode": self.vscode_var.get()
        })
        
        # Save configuration
        if self.save_config():
            self.status_var.set("✅ Configuration saved successfully!")
            self.root.after(2000, lambda: self.status_var.set("Ready"))  # Clear after 2 seconds
            messagebox.showinfo("Success", "Configuration saved successfully!\n\nRestart the application for changes to take effect.")
            self.root.quit()
    
    def test_connection(self):
        """Test proxy connection"""
        server = self.server_var.get().strip()
        port = self.port_var.get().strip()
        
        if not server or not port:
            messagebox.showerror("Error", "Please enter proxy server and port")
            return
        
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((server, int(port)))
            sock.close()
            
            if result == 0:
                self.status_var.set("✅ Connection successful!")
                self.root.after(3000, lambda: self.status_var.set("Ready"))
                messagebox.showinfo("Success", "Proxy connection test successful!")
            else:
                self.status_var.set("❌ Connection failed!")
                self.root.after(3000, lambda: self.status_var.set("Ready"))
                messagebox.showwarning("Warning", "Cannot connect to proxy server")
        except Exception as e:
            self.status_var.set(f"❌ Test failed: {str(e)[:30]}...")
            self.root.after(3000, lambda: self.status_var.set("Ready"))
            messagebox.showerror("Error", f"Connection test failed: {e}")
    
    def run(self):
        """Run the configuration GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ProxyConfigGUI()
    app.run()
