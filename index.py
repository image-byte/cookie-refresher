from flask import Flask, request
import threading
import requests
import time

app = Flask(__name__)

# Globals (avoid hardcoding tokens!)
BOT_TOKEN = MTM1OTA1Njc2ODc3NjQwOTE5MQ.GEGHqB.aEcwGjF50touLmNJId99QWQA70sUdM58mtnthU
BOT_STATUS = "🔴 Offline"

def run_bot():
    global BOT_STATUS
    headers = {"Authorization": f"Bot {BOT_TOKEN}"}
    
    while True:
        try:
            # Example: Check bot status (replace with your bot logic)
            response = requests.get(
                "https://discord.com/api/v10/users/@me",
                headers=headers
            )
            if response.status_code == 200:
                BOT_STATUS = "🟢 Online"
            else:
                BOT_STATUS = "🔴 Error"
            
            print(f"Bot is {BOT_STATUS} | Pinged Discord API")
            time.sleep(60)  # Check every minute
            
        except Exception as e:
            print(f"Bot error: {e}")
            BOT_STATUS = "🔴 Crash"
            time.sleep(10)

@app.route('/')
def home():
    return f"""
    <h1>Discord Bot Keeper</h1>
    <p>Status: {BOT_STATUS}</p>
    <p>Add ?token=YOUR_BOT_TOKEN to start the bot.</p>
    """

@app.route('/start')
def start_bot():
    global BOT_TOKEN, BOT_STATUS
    BOT_TOKEN = request.args.get('token')
    
    if not BOT_TOKEN:
        return "❌ Error: No token provided. Add ?token=YOUR_BOT_TOKEN"
    
    # Start bot in background
    if threading.active_count() == 1:  # Only start if not running
        threading.Thread(target=run_bot, daemon=True).start()
        BOT_STATUS = "🟠 Starting..."
        return "✅ Bot started! Visit / to check status."
    else:
        return "⚠️ Bot already running!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
