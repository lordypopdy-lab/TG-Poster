import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient, events

# === Configure your two accounts ===
accounts = [
    {
        "session": "account_avnbvnb",
        "api_id": 26439312,  # replace with your API ID
        "api_hash": "66dad0ce553094675ec64d87de13ddd8"
    },
    {
        "session": "account_bg0987vb",
        "api_id": 29946177,  # replace with your API ID
        "api_hash": "0000ed64d3e0dd9fa2036ea48b05b4db"
    }
]

# === Channel info ===
SOURCE_CHANNEL = '@Xmcryptonews'
DEST_CHANNEL = '@BitclubCryptoNews'

# === Rotation settings ===
ROTATION_INTERVAL_HOURS = 24

# === Global vars ===
current_account_index = 0
client = None
start_time = datetime.now()


async def forward_handler(event):
    try:
        await client.send_message(DEST_CHANNEL, event.message)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Message forwarded.")
    except Exception as e:
        print(f"Error forwarding message: {e}")


async def check_rotation():
    global current_account_index, client, start_time
    while True:
        if datetime.now() - start_time >= timedelta(hours=ROTATION_INTERVAL_HOURS):
            print("🔄 Rotating account...")

            await client.disconnect()

            current_account_index = (current_account_index + 1) % len(accounts)
            start_time = datetime.now()

            client = await start_client()
        await asyncio.sleep(5)  # low impact polling


async def start_client():
    acc = accounts[current_account_index]
    print(f"🚀 Starting client: {acc['session']}")
    new_client = TelegramClient(acc["session"], acc["api_id"], acc["api_hash"])
    await new_client.start()
    new_client.add_event_handler(forward_handler, events.NewMessage(chats=SOURCE_CHANNEL))
    return new_client


async def main():
    global client
    client = await start_client()
    await asyncio.gather(
        client.run_until_disconnected(),
        check_rotation()
    )


if __name__ == "__main__":
    asyncio.run(main())
