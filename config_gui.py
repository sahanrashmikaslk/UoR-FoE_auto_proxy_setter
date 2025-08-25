import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from pathlib import Path

class ProxyConfigGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Uni-Proxy Manager Configuration")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Configuration file path
        self.config_file = Path(__file__).parent / "proxy_config.json"
        
        # Load existing configuration
        self.config = self.load_config()
        
        self.create_widgets()
        self.load_values()
    
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
        """Create GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Proxy Settings Section
        proxy_frame = ttk.LabelFrame(main_frame, text="Proxy Settings", padding="10")
        proxy_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(proxy_frame, text="Proxy Server:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.server_var = tk.StringVar()
        server_entry = ttk.Entry(proxy_frame, textvariable=self.server_var, width=30)
        server_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(proxy_frame, text="Port:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.port_var = tk.StringVar()
        port_entry = ttk.Entry(proxy_frame, textvariable=self.port_var, width=10)
        port_entry.grid(row=1, column=1, sticky=tk.W, pady=(0, 5))
        
        # Application Settings Section
        app_frame = ttk.LabelFrame(main_frame, text="Application Settings", padding="10")
        app_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.auto_start_var = tk.BooleanVar()
        ttk.Checkbutton(app_frame, text="Start with Windows", 
                       variable=self.auto_start_var).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Proxy Target Settings Section
        target_frame = ttk.LabelFrame(main_frame, text="Proxy Targets", padding="10")
        target_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.windows_var = tk.BooleanVar()
        ttk.Checkbutton(target_frame, text="Windows System Proxy", 
                       variable=self.windows_var).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.git_var = tk.BooleanVar()
        ttk.Checkbutton(target_frame, text="Git Configuration", 
                       variable=self.git_var).grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.npm_var = tk.BooleanVar()
        ttk.Checkbutton(target_frame, text="npm Configuration", 
                       variable=self.npm_var).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.vscode_var = tk.BooleanVar()
        ttk.Checkbutton(target_frame, text="VS Code Settings", 
                       variable=self.vscode_var).grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(button_frame, text="Save", command=self.save_settings).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Cancel", command=self.root.quit).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Test Connection", command=self.test_connection).pack(side=tk.LEFT, padx=(0, 5))
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        proxy_frame.columnconfigure(1, weight=1)
    
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
            self.status_var.set("Configuration saved successfully!")
            messagebox.showinfo("Success", "Configuration saved successfully!")
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
                self.status_var.set("Connection successful!")
                messagebox.showinfo("Success", "Proxy connection test successful!")
            else:
                self.status_var.set("Connection failed!")
                messagebox.showwarning("Warning", "Cannot connect to proxy server")
        except Exception as e:
            self.status_var.set(f"Test failed: {e}")
            messagebox.showerror("Error", f"Connection test failed: {e}")
    
    def run(self):
        """Run the configuration GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ProxyConfigGUI()
    app.run()
