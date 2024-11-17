# HotwheelsPDF

A Hot Rod themed PDF manipulation tool with a flame-inspired interface! 🔥

## Features

- Split PDF files into individual pages
- Merge multiple PDFs into a single document
- Rotate PDF pages with live preview
- Hot Rod themed interface with dynamic flame effects
- Cross-platform support (Windows, macOS)

## Installation Guide

### Windows Users
1. Go to the [Releases](https://github.com/Skod4/HotwheelsPDF/releases) page
2. Download the latest `HotwheelsPDF-Windows.exe`
3. Double-click the downloaded file to run the application

Note: When running for the first time, Windows might show a SmartScreen warning. This happens because the app is new and not yet widely distributed. To run anyway:
1. Click "More info"
2. Click "Run anyway"
3. You only need to do this once

### Mac Users
1. Go to the [Releases](https://github.com/Skod4/HotwheelsPDF/releases) page
2. Download the latest `HotwheelsPDF-Mac.dmg`
3. Double-click the downloaded DMG file
4. **Important**: Drag HotwheelsPDF to your Applications folder
   - Don't run the app directly from the DMG
   - Running from Applications ensures proper permissions

#### First Time Setup on macOS
When launching for the first time, you'll need to bypass macOS security measures:

1. **If you see "app cannot be opened because it is from an unidentified developer":**
   - Right-click (or Control-click) HotwheelsPDF in Applications
   - Select "Open" from the menu
   - Click "Open" in the security dialog
   - This step is only needed once

2. **If the app is blocked in Security & Privacy:**
   - Open System Preferences > Security & Privacy
   - Click the lock icon to make changes (you'll need your password)
   - Look for "HotwheelsPDF was blocked from use"
   - Click "Open Anyway"
   - Follow the steps above to open the app

After completing these steps once, you can open HotwheelsPDF normally by double-clicking.

#### Troubleshooting on macOS
If you're having issues:
1. Make sure you're running the app from Applications folder
2. Check System Preferences > Security & Privacy for any blocked permissions
3. If the app won't open at all:
   - Open Terminal
   - Type: `xattr -cr /Applications/HotwheelsPDF.app`
   - Try opening the app again

## For Developers (From Source)

If you want to run from source or contribute to development:

```bash
# Clone the repository
git clone https://github.com/Skod4/HotwheelsPDF.git
cd HotwheelsPDF

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

## Usage

1. Launch HotwheelsPDF
2. Choose your desired operation:
   - Split PDF: Split a PDF into individual pages
   - Merge PDFs: Combine multiple PDFs into one
   - Rotate PDF: Rotate pages with live preview

## License

This project is licensed under the MIT License - see the LICENSE file for details.
