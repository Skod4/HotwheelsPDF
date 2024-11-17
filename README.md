# HotwheelsPDF

🔥

## Features

- Split PDF files into individual pages
- Merge multiple PDFs into a single document
- Rotate PDF pages with live preview
- Cross-platform support (Windows, macOS)

## Easy Installation (No Python Required)

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
4. Drag HotwheelsPDF to your Applications folder
5. First time setup:
   - Go to Applications folder
   - Right-click (or Control-click) HotwheelsPDF
   - Select "Open" from the menu
   - Click "Open" in the security dialog
   - This step is only needed once

#### Troubleshooting macOS Installation
If you see "App can't be opened because it is from an unidentified developer":
1. Click Apple menu () > System Settings
2. Click Privacy & Security in the sidebar
3. Scroll down to Security
4. Next to "HotwheelsPDF was blocked from use because it is not from an identified developer," click Open Anyway
5. Click Open in the confirmation dialog

If the app is "damaged":
1. Open Terminal (Applications > Utilities > Terminal)
2. Run this command (you'll need to enter your password):
   ```bash
   xattr -cr /Applications/HotwheelsPDF.app
   ```
3. Try opening the app again

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
