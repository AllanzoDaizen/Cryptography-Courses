"""
Setup script for the ransomware demo
Creates test environment and verifies dependencies
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['cryptography', 'flask', 'requests', 'psutil']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    return missing_packages

def create_test_environment():
    """Create test files and directory structure"""
    print("\n[*] Creating test environment...")
    
    # Create directories
    directories = ['data', 'test_files', 'assets', 'docs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Create test files
    test_files = {
        "test_files/document1.txt": "This is an important business document.\nContains confidential company information.\n",
        "test_files/financial_data.xlsx": "Financial records and accounting data.\nQ4 2024 projections and revenue reports.\n",
        "test_files/family_photo.jpg": "This would be a family photo in real scenario.\nFor demo purposes, it's just text.\n",
        "test_files/important_data.pdf": "Critical project documentation and plans.\nSensitive intellectual property content.\n"
    }
    
    for file_path, content in test_files.items():
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Created test file: {file_path}")
    
    print("\n✅ Test environment setup complete!")

def generate_encryption_keys():
    """Generate RSA key pair"""
    print("\n[*] Generating encryption keys...")
    try:
        from src.key_generator import generate_rsa_keypair
        generate_rsa_keypair()
        print("✅ Encryption keys generated successfully!")
    except Exception as e:
        print(f"❌ Failed to generate keys: {e}")
        return False
    return True

def main():
    print("=" * 60)
    print("🔴 RED TEAM RANSOMWARE DEMO - SETUP")
    print("⚠️  EDUCATIONAL USE ONLY - ISOLATED LAB REQUIRED")
    print("=" * 60)
    
    # Check Python version
    print(f"\n[*] Python version: {sys.version}")
    
    # Check dependencies
    print("\n[*] Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("[*] Installing required packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run: pip install -r requirements.txt")
            return
    
    # Create test environment
    create_test_environment()
    
    # Generate keys
    if not generate_encryption_keys():
        print("❌ Setup failed - could not generate encryption keys")
        return
    
    print("\n" + "=" * 60)
    print("✅ SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\n🎯 Next steps:")
    print("1. Start C2 server: python src/c2_gui_server.py")
    print("2. Run demo: python demo.py")
    print("3. Access dashboard: http://localhost:5000")
    print("\n📚 Educational resources in docs/ directory")
    print("⚠️  Remember: This is for educational purposes only!")

if __name__ == "__main__":
    main()