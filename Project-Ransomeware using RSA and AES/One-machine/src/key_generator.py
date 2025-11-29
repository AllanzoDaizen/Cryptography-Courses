"""
RSA Key Pair Generator
Educational Use Only
"""

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import os

def generate_rsa_keypair():
    """Generate RSA public/private key pair for demo"""
    print("[*] Generating RSA 2048-bit key pair...")
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Get public key
    public_key = private_key.public_key()
    
    # Serialize private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serialize public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Save keys
    with open("data/private_key.pem", "wb") as f:
        f.write(private_pem)
    
    with open("data/public_key.pem", "wb") as f:
        f.write(public_pem)
    
    print("[+] RSA keys generated and saved to data/ directory")
    print("[+] Private key: data/private_key.pem")
    print("[+] Public key: data/public_key.pem")
    
    return public_pem, private_pem

if __name__ == "__main__":
    generate_rsa_keypair()