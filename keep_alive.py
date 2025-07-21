from flask import Flask, jsonify, request
import threading
import datetime
import time
import os

app = Flask(__name__)

# Track bot activity and statistics
bot_stats = {
    'start_time': datetime.datetime.now(),
    'last_ping': datetime.datetime.now(),
    'ping_count': 0,
    'uptime_checks': 0,
    'external_pings': 0
}

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
                <strong>Bot Name:</strong> Auto Lock Thread Bot<br>
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
        "name": "Auto Lock Thread Bot",
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
    global bot_stats
    bot_stats['last_ping'] = datetime.datetime.now()
    bot_stats['ping_count'] += 1
    
    # Check if this is an external monitoring service
    user_agent = request.headers.get('User-Agent', '')
    if any(monitor in user_agent.lower() for monitor in ['uptimerobot', 'pingdom', 'monitor', 'uptime']):
        bot_stats['external_pings'] += 1
    
    return jsonify({
        "response": "pong",
        "status": "alive",
        "timestamp": datetime.datetime.now().isoformat(),
        "message": "Bot is responding to ping!",
        "uptime_seconds": int((datetime.datetime.now() - bot_stats['start_time']).total_seconds()),
        "ping_count": bot_stats['ping_count']
    })

@app.route('/health')
def health():
    return jsonify({
        "health": "ok",
        "service": "discord_bot",
        "status": "running"
    })

@app.route('/uptime')
def uptime():
    """Detailed uptime statistics for external monitoring"""
    global bot_stats
    uptime_seconds = int((datetime.datetime.now() - bot_stats['start_time']).total_seconds())
    uptime_hours = uptime_seconds // 3600
    uptime_days = uptime_hours // 24
    
    return jsonify({
        "uptime": {
            "seconds": uptime_seconds,
            "hours": uptime_hours,
            "days": uptime_days,
            "formatted": f"{uptime_days}d {uptime_hours % 24}h {(uptime_seconds % 3600) // 60}m"
        },
        "statistics": {
            "total_pings": bot_stats['ping_count'],
            "external_pings": bot_stats['external_pings'],
            "last_ping": bot_stats['last_ping'].isoformat(),
            "start_time": bot_stats['start_time'].isoformat()
        },
        "monitoring": {
            "recommended_interval": "5 minutes",
            "ping_url": request.host_url + "ping",
            "status_url": request.host_url + "status"
        }
    })

def run():
    app.run(host='0.0.0.0', port=5000, debug=False)

def keep_alive():
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    print("Keep-alive web server started on port 5000")
