# adb-info
 Android phone adb information
# Device Info Checker 🔍

[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows|Linux|macOS](https://img.shields.io/badge/platform-Windows%20|%20Linux%20|%20macOS-lightgrey.svg)](https://www.android.com/)

A cross-platform GUI application to retrieve detailed Android device information using ADB, with automatic ADB/Fastboot installation capabilities.

![Screenshot](![image](https://github.com/user-attachments/assets/40f30877-7446-4387-a428-88c5a2e58360)
) <!-- Add actual screenshot later -->

## Features ✨

- **Cross-platform Support** (Windows, macOS, Linux)
- Automatic ADB/Fastboot installation
- Device selection dropdown with auto-refresh
- Organized device information categories:
  - Basic Info
  - Security Details
  - Hardware Specifications
  - Network Information
- Real-time logging and error reporting
- Export capability for logs and device info
- Windows-specific enhancements:
  - Installs to `C:\Android\platform-tools`
  - Automatic PATH configuration
  - Admin-friendly system integration

## Installation ⚙️

### Prerequisites
- Python 3.6 or higher
- Internet connection (for initial setup)

```bash
# Install required packages
pip install requests

python device_info_checker.py

Connect your Android device with USB debugging enabled

Refresh connected devices:

Click "Refresh Devices" button

Check device information:

Select device from dropdown

Click "Check Device Info"

Export logs:

Click "Export Log" to save information

Windows Specific Notes 🖥️
Installation Path:


C:\Android\platform-tools
Administrator Rights recommended for:

Permanent PATH configuration

System-wide ADB/Fastboot access

Directory Structure:

C:\Android\platform-tools\
├── adb.exe
├── fastboot.exe
└── other platform tools...
Development 🛠️
Requirements
Python 3.6+

ADB-enabled Android device

Windows: Administrator privileges for full functionality

bash
Copy
# Clone repository
git clone https://github.com/yourusername/device-info-checker.git
cd device-info-checker

# Install dependencies
pip install -r requirements.txt
Logging
Logs stored in device_info.log

Export logs to device_info_export.txt

License 📄
This project is licensed under the MIT License - see the LICENSE file for details.

Note: Always ensure proper authorization before accessing devices. The developers are not responsible for any device configuration changes made using this tool.

🔧 Built with Python and Tkinter | 📧 Contact: your.rdxhacker8591@gmail.com


Key elements included:
1. Clear badges for quick project understanding
2. Organized feature list with platform-specific notes
3. Step-by-step installation and usage instructions
4. Windows-specific configuration details
5. Development setup guidelines
6. License information and disclaimer
7. Responsive formatting for GitHub Markdown

To complete the README:
1. Add actual screenshots of your application
2. Update placeholder contact information
3. Replace repository URL in development section
4. Consider adding:
   - Troubleshooting section
   - FAQ section
   - Contribution guidelines
   - Code of conduct
   - Acknowledgements

The README follows standard GitHub formatting and provides all essential information while maintaining readability.
