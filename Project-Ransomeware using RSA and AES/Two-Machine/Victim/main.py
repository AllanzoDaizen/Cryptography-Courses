#!/usr/bin/env python3
"""
Victim Side Controller - Run this on Windows VM
"""

import os
import sys

def main():
    print("="*60)
    print("🎯 RANSOMWARE SIMULATION - VICTIM CONTROLLER")
    print("⚠️  FOR EDUCATIONAL USE IN VM ONLY!")
    print("="*60)
    
    print("\n📋 Options:")
    print("1. Run ransomware simulation (encrypt files)")
    print("2. Run decryptor (recover files with key)")
    print("3. Build executable from ransomware.py")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        # Run the ransomware simulation
        try:
            from src.ransomware import VictimRansomware
            print("\n[⚠️] Starting ransomware simulation...")
            print("[⚠️] This will encrypt files in current directory!")
            confirm = input("\nAre you in a Windows VM? (yes/no): ").lower()
            if confirm == 'yes':
                malware = VictimRansomware()
                malware.run()
            else:
                print("Operation cancelled. Only run in VM!")
        except Exception as e:
            print(f"Error: {e}")
            print("Make sure src/ransomware.py exists")
    
    elif choice == "2":
        # Run the decryptor
        try:
            from src.decryptor import main as decryptor_main
            decryptor_main()
        except Exception as e:
            print(f"Error: {e}")
            print("Make sure src/decryptor.py exists")
    
    elif choice == "3":
        # Build executable (for Windows)
        print("\nBuilding executable...")
        if os.path.exists("src/build_exe.sh"):
            os.system("bash src/build_exe.sh")
        else:
            print("\nFor Windows, run these commands:")
            print("cd src")
            print("pip install pyinstaller")
            print("pyinstaller --onefile --noconsole ransomware.py")
            print("\nExecutable will be in: src/dist/ransomware.exe")
    
    elif choice == "4":
        print("\nExiting...")
        return
    
    else:
        print("\nInvalid choice!")
    
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()