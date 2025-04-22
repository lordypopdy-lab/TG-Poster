import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient, events

# === Account credentials ===
accounts = [
    {
        "session": "account_avnbvnb",
        "api_id": 26439312,
        "api_hash": "66dad0ce553094675ec64d87de13ddd8"
    },
    {
        "session": "account_bg0987vb",
        "api_id": 29946177,
        "api_hash": "0000ed64d3e0dd9fa2036ea48b05b4db"
    }
]

# === Channels ===
SOURCE_CHANNEL = '@Xmcryptonews'
DEST_CHANNEL = '@BitclubCryptoNews'

# === Rotation setup ===
ROTATION_INTERVAL = timedelta(hours=24)

# Globals
clients = [None, None]
handlers = [None, None]
current_index = 0
last_rotation = datetime.now()


def make_handler(index):
    async def handler(event):
        try:
            await clients[index].send_message(DEST_CHANNEL, event.message)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {accounts[index]['session']} forwarded message.")
        except Exception as e:
            print(f"Error from {accounts[index]['session']}: {e}")
    return handler


async def setup_clients():
    for i in range(2):
        acc = accounts[i]
        print(f"🔐 Logging in: {acc['session']}")
        clients[i] = TelegramClient(acc['session'], acc['api_id'], acc['api_hash'])
        await clients[i].start()


async def start_forwarding(index):
    handlers[index] = make_handler(index)
    clients[index].add_event_handler(handlers[index], events.NewMessage(chats=SOURCE_CHANNEL))
    print(f"✅ Forwarding enabled on {accounts[index]['session']}")


async def stop_forwarding(index):
    if handlers[index]:
        clients[index].remove_event_handler(handlers[index])
        print(f"⛔ Forwarding stopped on {accounts[index]['session']}")


async def rotate():
    global current_index, last_rotation
    while True:
        if datetime.now() - last_rotation >= ROTATION_INTERVAL:
            await stop_forwarding(current_index)
            current_index = (current_index + 1) % 2
            await start_forwarding(current_index)
            last_rotation = datetime.now()
        await asyncio.sleep(5)


async def main():
    await setup_clients()
    await start_forwarding(current_index)

    await asyncio.gather(
        clients[0].run_until_disconnected(),
        clients[1].run_until_disconnected(),
        rotate()
    )


if __name__ == "__main__":
    asyncio.run(main())
