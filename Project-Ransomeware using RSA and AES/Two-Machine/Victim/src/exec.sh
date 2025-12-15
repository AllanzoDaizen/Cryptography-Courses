# Install mingw cross-compiler
sudo apt update
sudo apt install mingw-w64e

# OR if using PyInstaller with wine:
sudo apt install wine

wine pyinstaller --onefile --noconsole ransomware.py
