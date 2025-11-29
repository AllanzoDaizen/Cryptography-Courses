# 🔴 Red Team Ransomware Demo

> **⚠️ EDUCATIONAL PURPOSE ONLY - ISOLATED LAB ENVIRONMENT REQUIRED ⚠️**

A complete hybrid cryptography ransomware demonstration for red team training and cybersecurity education.

## 🎯 Features

- **Hybrid Cryptography**: RSA + AES encryption
- **C2 Communication**: Command and Control server with web dashboard
- **GUI Components**: Fake security scanner & decryptor tools
- **Realistic TTPs**: Mimics actual ransomware behavior
- **Full Lifecycle**: Infection → Encryption → Payment → Decryption

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Isolated lab environment (VM recommended)
- No network connection to production systems

### Installation
```bash
# Extract the package
unzip redteam-ransomware-demo.zip
cd redteam-ransomware-demo

# Install dependencies
pip install -r requirements.txt

# Generate encryption keys
python src/key_generator.py

# Create test environment
python setup.py