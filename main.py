import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import platform
import os
import sys
import zipfile
import requests
import logging
from threading import Thread

class DeviceInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Device Info Checker")
        self.root.geometry("800x600")
        
        # Configure logging
        logging.basicConfig(filename='device_info.log', level=logging.INFO)
        self.logger = logging.getLogger()
        
        # Initialize UI
        self.create_widgets()
        self.check_environment()
        
        # Auto-check devices when starting
        self.refresh_devices()

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Device selection
        ttk.Label(main_frame, text="Connected Devices:").pack(anchor=tk.W)
        self.device_combobox = ttk.Combobox(main_frame, state='readonly')
        self.device_combobox.pack(fill=tk.X, pady=5)
        
        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Refresh Devices", command=self.refresh_devices).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Check Device Info", command=self.check_info).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Export Log", command=self.export_log).pack(side=tk.RIGHT)

        # Info display
        self.log_text = tk.Text(main_frame, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def check_environment(self):
        """Check for ADB and Fastboot installation"""
        try:
            self.execute_command("adb --version")
            self.execute_command("fastboot --version")
        except Exception as e:
            self.logger.error(f"Environment check failed: {str(e)}")
            if messagebox.askyesno("Missing Dependencies", 
                                 "ADB/Fastboot not found. Install automatically to C:\\Android\\platform-tools?"):
                self.install_adb_automatically()
            else:
                messagebox.showerror("Error", "ADB/Fastboot required")
                sys.exit(1)

    def execute_command(self, command):
        """Execute a shell command with error handling"""
        try:
            result = subprocess.run(command, shell=True, check=True,
                                  capture_output=True, text=True, timeout=10)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {command}\nError: {e.stderr}")
            raise

    def refresh_devices(self):
        """Refresh list of connected devices"""
        self.status_bar.config(text="Refreshing devices...")
        try:
            output = self.execute_command("adb devices")
            devices = [line.split("\t")[0] for line in output.splitlines() if "\tdevice" in line]
            self.device_combobox['values'] = devices
            self.device_combobox.set(devices[0] if devices else "")
            self.status_bar.config(text=f"Found {len(devices)} devices")
        except Exception as e:
            self.log_error(f"Error refreshing devices: {str(e)}")

    def check_info(self):
        """Check device information for selected device"""
        device = self.device_combobox.get()
        if not device:
            messagebox.showerror("Error", "No device selected!")
            return

        Thread(target=self._check_info_thread, args=(device,), daemon=True).start()

    def _check_info_thread(self, device):
        """Background thread for checking device info"""
        self.status_bar.config(text="Fetching device info...")
        try:
            info = self.get_device_info(device)
            self.display_info(info)
            self.status_bar.config(text="Device info fetched successfully")
        except Exception as e:
            self.log_error(f"Error checking info: {str(e)}")

    def get_device_info(self, device):
        """Retrieve device information using ADB"""
        props = {
            "Basic Info": {
                "ro.product.manufacturer": "Manufacturer",
                "ro.product.brand": "Brand",
                "ro.product.model": "Model",
                "ro.product.name": "Product Name",
                "ro.boot.slot_suffix": "Slot",
                "ro.build.version.release": "Android Version",
                "ro.build.version.sdk": "SDK Version",
                "ro.build.id": "Build ID",
                "ro.build.display.id": "Display ID",
                "ro.build.version.incremental": "Incremental Version",
                "ro.build.fingerprint": "Fingerprint",
                "ro.build.type": "Build Type",
                "ro.build.tags": "Build Tags",
                "ro.build.flavor": "Build Flavor",
                "ro.build.description": "Build Description",
                "ro.build.characteristics": "Build Characteristics",
                "ro.build.date": "Build Date",  
                "ro.boot.mode": "BootMode",
        "ro.boot.product.hardware.sku": "Product Hardware SKU",
        "ro.boot.product.name": "Product Name",
        
                
            },
            "Security": {
               "ro.build.version.security_patch": "Security Patch",
                "ro.boot.verifiedbootstate": "Boot State",
                "ro.boot.flash.locked": "Bootloader Locked",
                "ro.rom.zone": "ROM Zone",
        "ro.secure": "Secure",
        "ro.secureboot.devicelock": "Device Lock",
        "ro.secureboot.lockstate": "Lock State",
        "ro.crypto.state": "Crypto State",
        "gsm.version.baseband": "Baseband",
        "ro.system_ext.build.version.release": "SystemExtRelease",
        "ro.boot.flash.locked": "FlashLocked",
        "ro.boot.force_normal_boot": "ForceNormalBoot",
        "ro.boot.meta_log_disable": "MetaLogDisable",
            },
            "Hardware": {
               "ro.hardware": "Hardware",
                "ro.board.platform": "Board Platform",
                "ro.soc.manufacturer": "SoC Manufacturer",
                "ro.soc.model": "SoC Model",
                "ro.boot.hardware": "Hardware",
         "ro.soc.manufacturer": "SOCManufacturer",
        "ro.soc.model": "SOCModel",
        "ro.soc.platform": "SOCPlatform",
        "ro.board.platform": "BoardPlatform",
        "ro.boot.serialno": "SerialNo",
        "ro.snowflake.deviceid": "DeviceID",
         "ro.ril.oem.psno": "PSNO",
        "ro.ril.oem.sno": "SNO",
        "ro.ril.oem.sw_ver": "SWVer",
        "ro.boot.hwc": "HWC",
        "ro.boot.hwlevel": "HW Level",
        "ro.boot.hwversion": "HW Version",
            },
            "Network": {
                 "ro.boot.carrierid": "Carrier ID",
                  "ro.product.cpu.abi": "CPU",
        "ro.ril.miui.imei0": "IMEI0",
        "ro.ril.miui.imei1": "IMEI1",
        "ro.ril.oem.imei": "OEM IMEI",
        "ro.ril.oem.imei1": "OEM IMEI1",
        "ro.ril.oem.imei2": "OEM IMEI2",
         "gsm.sim.operator.iso-country": "ISO Country",
        "gsm.sim.operator.numeric": "Operator Numeric",
        "gsm.sim.operator.alpha": "Operator Alpha",
        "gsm.sim.operator.alpha-short": "Operator Alpha Short",
        "gsm.sim.operator.numeric": "Operator Numeric",
        "gsm.sim.state": "SIM State",
        "gsm.operator.alpha": "Operator Roming",
        "gsm.operator.alpha-short": "Operator Roming Short",
        "gsm.operator.numeric": "Operator Numeric",
        "gsm.sim.operator.alpha": "Carrier",
        "gsm.version.baseband": "Baseband Version",
                "gsm.version.ril-impl": "RIL Implementation",
            }
        }

        info = {}
        for category, properties in props.items():
            info[category] = {}
            for prop, name in properties.items():
                value = self.execute_command(f"adb -s {device} shell getprop {prop}")
                info[category][name] = value if value else "N/A"
        return info

    def display_info(self, info):
        """Display formatted information in the text widget"""
        self.log_text.delete(1.0, tk.END)
        for category, properties in info.items():
            self.log_text.insert(tk.END, f"\n=== {category} ===\n", 'header')
            for name, value in properties.items():
                self.log_text.insert(tk.END, f"{name}: {value}\n")

    def install_adb_automatically(self):
        """Install ADB and Fastboot automatically to C:\Android\platform-tools"""
        try:
            self.status_bar.config(text="Downloading platform-tools...")
            os_name = platform.system().lower()
            url = {
                "windows": "https://dl.google.com/android/repository/platform-tools-latest-windows.zip",
                "darwin": "https://dl.google.com/android/repository/platform-tools-latest-darwin.zip",
                "linux": "https://dl.google.com/android/repository/platform-tools-latest-linux.zip"
            }[os_name]

            install_path = {
                "windows": r"C:\Android\platform-tools",
                "darwin": os.path.expanduser("~/Library/Android/platform-tools"),
                "linux": os.path.expanduser("~/Android/platform-tools")
            }[os_name]

            os.makedirs(install_path, exist_ok=True)
            zip_path = os.path.join(install_path, "platform-tools.zip")
            
            # Download with progress
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(zip_path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress = downloaded / total_size
                    self.status_bar.config(text=f"Downloading... {progress:.0%}")

            # Extract and update PATH
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(install_path)
            
            # Update environment variables
            os.environ['PATH'] += os.pathsep + os.path.join(install_path, 'platform-tools')
            os.remove(zip_path)
            
            # Windows-specific permanent PATH update
            if os_name == "windows":
                self.add_to_system_path(r"C:\Android\platform-tools")
            
            messagebox.showinfo("Success", "ADB/Fastboot installed successfully in C:\\Android\\platform-tools")
            self.refresh_devices()
            
        except Exception as e:
            self.log_error(f"Installation failed: {str(e)}")
            messagebox.showerror("Error", f"Installation failed: {str(e)}")

    def add_to_system_path(self, path):
        """Add directory to system PATH permanently (Windows only)"""
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                                0, winreg.KEY_ALL_ACCESS)
            
            current_path, _ = winreg.QueryValueEx(key, "Path")
            if path not in current_path:
                new_path = current_path + ";" + path
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                winreg.CloseKey(key)
                
                # Broadcast environment change
                import ctypes
                ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x1A, 0, "Environment", 0, 1000, None)
        except Exception as e:
            self.log_error(f"Failed to update system PATH: {str(e)}")
            messagebox.showwarning("PATH Update", 
                                  "Couldn't update system PATH permanently. Run as Administrator for system-wide access.")

    def export_log(self):
        """Export log to file"""
        try:
            with open('device_info.log', 'r') as f:
                log_content = f.read()
            with open('device_info_export.txt', 'w') as f:
                f.write(log_content)
            messagebox.showinfo("Success", "Log exported to device_info_export.txt")
        except Exception as e:
            self.log_error(f"Export failed: {str(e)}")

    def log_error(self, message):
        """Handle error messages"""
        self.logger.error(message)
        self.status_bar.config(text=message)
        messagebox.showerror("Error", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = DeviceInfoApp(root)
    
    # Configure text tags
    app.log_text.tag_config('header', foreground='blue', font=('Arial', 10, 'bold'))
    
    root.mainloop()