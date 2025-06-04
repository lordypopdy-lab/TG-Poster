from flask import Flask
import threading
import asyncio
from telethon import TelegramClient, events

# === Telegram credentials ===
api_id = 22037936
api_hash = '68d953559a91f655ff88794625b5cb75'

# === Channels ===
source_channel = '@xmcryptonews'
target_channel = '@BitclubCryptoNews'

# === Telethon client ===
client = TelegramClient('poster001', api_id, api_hash)

# === Flask web server to keep Replit alive ===
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram forwarder is running! Now...", 200

def run_web():
    app.run(host='0.0.0.0', port=8080)

@client.on(events.NewMessage(chats=source_channel))
async def forward_handler(event):
    try:
        await client.forward_messages(target_channel, event.message)
        print(f"Forwarded message ID {event.message.id}")
    except Exception as e:
        print(f"Error forwarding message: {e}")

def start():
    try:
        client.start()
        client.run_until_disconnected()
    except Exception as e:
        print("Client failed to start:", e)

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    start()
