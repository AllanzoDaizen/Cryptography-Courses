# Ransomware Simulation - Usage Guide

> ⚠️ **FOR EDUCATIONAL USE ONLY** - Use only in isolated virtual machines!

## Quick Setup (5 Minutes)

### Prerequisites
- Kali Linux VM (Attacker)
- Windows 10/11 VM (Victim)
- Both VMs on same network
- Python 3.8+ installed on both

---

## Step-by-Step Usage

### 1️⃣ Attacker Setup (Kali Linux)

Open terminal and install dependencies:


```bash
cd Attacker
pip -r install requirements.txt
```

Then run:

```bash
python3 main.py
```

The toolkit will automatically:
- ✅ Generate RSA encryption keys
- ✅ Detect your Kali IP address but you should manully input it
- ✅ Start C2 server on port 5000
- ✅ Build Windows payload
- ✅ Open dashboard in browser

**Important:** Note your Kali IP address shown on screen!

---

### 2️⃣ Transfer Payload to Windows

Copy the `ransomware.py` file to your Windows VM:

**Option A: Shared Folder**
```bash
# Setup VirtualBox shared folder
# Copy from /Victim/src/ransomware.py
```

**Option B: Network Transfer**
```bash
# From Kali
scp Victim/src/ransomware.py user@<windows-ip>:C:\Users\user\
```

---

### 3️⃣ Run Ransomware (Windows)

Open Command Prompt or PowerShell:

```cmd
cd C:\path\to\ransomware
python ransomware.py
```

When prompted, type: `yes`

**What happens:**
1. Creates 5 test files (or uses existing files)
2. Encrypts them with AES-256
3. Renames to `.locked` extension
4. Contacts C2 server
5. Creates ransom note: `!!!READ_ME!!!.txt`

---

### 4️⃣ Monitor Victims (Kali Dashboard)

Open browser: `http://localhost:5000`

You'll see:
- Connected victims list
- Victim ID, OS, IP address
- Number of encrypted files
- Payment status
- Action buttons

**Get the decryption key:**
1. Click "Get Key" button for victim
2. Copy the Base64 key that appears
3. Save it for next step

---

### 5️⃣ Decrypt Files (Windows)

Copy `decryptor.py` `private_key.pem` to Windows (same folder as encrypted files):

```cmd
python decryptor.py
```

When prompted:
1. Type: `yes`
2. Paste the Base64 key from dashboard
3. Press Enter

**What happens:**
- Decrypts all `.locked` files
- Restores original filenames
- Removes encrypted versions
- Deletes ransom note

---

## Using the Interactive Menu

After initial setup, `main.py` shows this menu:

```
============================================================
🛠️  ATTACKER TOOLKIT MENU
============================================================
1. 👥 View/manage victims
2. 🖥️  Open C2 dashboard
3. 📋 Show victim database
4. 🔑 Show generated keys
5. 🚪 Exit
============================================================
```


## Testing Scenarios

### Scenario 1: Basic Attack (5 mins)
```
1. Start attacker toolkit
2. Run ransomware on Windows
3. Check dashboard for new victim
4. Get decryption key
5. Run decryptor
```

### Scenario 2: Multiple Victims (10 mins)
```
1. Setup 2 Windows VMs
2. Run ransomware on both
3. Dashboard shows both victims
4. Decrypt each separately
```

### Scenario 3: Offline Attack (7 mins)
```
1. Disconnect Windows VM network
2. Run ransomware (files encrypt locally)
3. Reconnect network
4. Victim registers with C2 automatically
```

---

## Troubleshooting

### Problem: "Module not found"
```bash
# On Kali
pip install -r requirements.txt

# On Windows
pip install cryptography requests
```

### Problem: "Can't contact C2 server"
1. Check Kali IP in `ransomware.py` (line 23)
2. Ping test: `ping <kali-ip>` from Windows
3. Verify C2 server is running: `netstat -tulpn | grep 5000`

### Problem: "Decryption failed"
1. Make sure you copied the FULL key (no spaces/truncation)
2. Verify `private_key.pem` is in same folder
3. Run Command Prompt as Administrator

### Problem: Dashboard won't open
```bash
# Manually start C2 server
cd Attacker/src
python3 c2_server.py
```

---

## File Locations

**After running main.py:**

```
Attacker/
├── Keys/
│   ├── private_key.pem    ← Keep secure!
│   └── public_key.pem     ← Embedded in payload
├── victims.db             ← Victim tracking
└── main.py                ← Start here

Victim/src/
├── ransomware.py          ← Run on Windows
└── decryptor.py           ← Recovery tool
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Start attacker | `python3 main.py` |
| Run ransomware | `python ransomware.py` |
| Decrypt files | `python decryptor.py` |
| View dashboard | `http://localhost:5000` |
| Check victims | Menu option 2 |



**Remember:** This is for learning only. Use responsibly in controlled environments!

