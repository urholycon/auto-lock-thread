from flask import Flask, jsonify
import threading
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>Discord Thread Lock Bot</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f0f0f0; }
            .container { background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: auto; }
            .status { color: #28a745; font-weight: bold; }
            .info { margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Discord Thread Lock Bot</h1>
            <p class="status">✅ Bot is running and active!</p>
            <div class="info">
                <strong>Bot Name:</strong> Auto Lock Thread#1010<br>
                <strong>Status:</strong> Online<br>
                <strong>Last Ping:</strong> """ + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """<br>
                <strong>Function:</strong> Auto-lock Discord threads with role-based permissions
            </div>
            <h3>Features:</h3>
            <ul>
                <li>Thread locking with "lock" or "lna" commands</li>
                <li>Delete/Keep buttons after locking</li>
                <li>Auto-delete for specific channels</li>
                <li>Role-based permission system</li>
                <li>24/7 uptime with keep-alive</li>
            </ul>
            <p><a href="/status">Check API Status</a> | <a href="/ping">Ping Bot</a></p>
        </div>
    </body>
    </html>
    """

@app.route('/status')
def status():
    return jsonify({
        "status": "online",
        "bot": "Discord Thread Lock Bot",
        "name": "Auto Lock Thread#1010",
        "uptime": True,
        "timestamp": datetime.datetime.now().isoformat(),
        "features": [
            "thread_locking",
            "auto_delete",
            "role_permissions",
            "keep_alive"
        ]
    })

@app.route('/ping')
def ping():
    return jsonify({
        "response": "pong",
        "status": "alive",
        "timestamp": datetime.datetime.now().isoformat(),
        "message": "Bot is responding to ping!"
    })

@app.route('/health')
def health():
    return jsonify({
        "health": "ok",
        "service": "discord_bot",
        "status": "running"
    })

def run():
    app.run(host='0.0.0.0', port=8080, debug=False)

def keep_alive():
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    print("Keep-alive web server started on port 8080")