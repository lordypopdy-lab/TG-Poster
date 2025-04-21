from telethon import TelegramClient, events
from datetime import datetime, timedelta
import asyncio
import time

# Account 1 credentials
api_id_1 = '22737247'
api_hash_1 = '5f4a3178c89e34aefc9027c3f04a98be'
session_name_1 = 'session1'

# Account 2 credentials
api_id_2 = '24772601'
api_hash_2 = '3132429a348ebdfb0cb6cea6f8100850'
session_name_2 = 'session2'

# Channel usernames or IDs
source_channel = '@Xmcryptonews'
destination_channel = '@BitclubCryptoNews'

# Time to switch accounts
switch_interval = timedelta(hours=24)

# Initialize clients
client1 = TelegramClient(session_name_1, api_id_1, api_hash_1)
client2 = TelegramClient(session_name_2, api_id_2, api_hash_2)

# Store the last time we switched
last_switch_time = datetime.now()
active_client = client1

async def main_loop():
    global active_client, last_switch_time

    await client1.start()
    await client2.start()

    print("Both clients started. Starting to monitor and forward messages.")

    @active_client.on(events.NewMessage(chats=source_channel))
    async def handler(event):
        await active_client.send_message(destination_channel, event.message)
        print(f"Forwarded message at {datetime.now()}")

    while True:
        now = datetime.now()
        if now - last_switch_time > switch_interval:
            print("Switching account...")
            if active_client == client1:
                client1.remove_event_handler(handler)
                active_client = client2
            else:
                client2.remove_event_handler(handler)
                active_client = client1

            # Re-assign event handler to new active client
            @active_client.on(events.NewMessage(chats=source_channel))
            async def handler(event):
                await active_client.send_message(destination_channel, event.message)
                print(f"Forwarded message at {datetime.now()}")

            last_switch_time = now

        await asyncio.sleep(10)

# Run the script
loop = asyncio.get_event_loop()
loop.run_until_complete(main_loop())