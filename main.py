from telethon import TelegramClient, events
import asyncio
import random

api_id = 14458814
api_hash = "b1e1a2ffd6000df2ea7b40517523bbbb"

source_channel = "xmcryptonews"
destination_channel = "@BitclubChatGroup"

# Telegram session names for different accounts
session_names = ["poster_session1", "poster_session2", "poster_session3"]
clients = []
message_counter = 0
current_index = 0
delay_seconds = (15, 30)  # Delay range between messages

# Track forwarded messages
forwarded_messages = {}

# Create and start all clients
for session in session_names:
    client = TelegramClient(session, api_id, api_hash)
    clients.append(client)

async def main():
    global message_counter, current_index

    for client in clients:
        await client.start()

    @clients[0].on(events.NewMessage(chats=source_channel))
    async def handler(event):
        global message_counter, current_index

        try:
            message_id = event.message.id

            if message_id in forwarded_messages:
                return

            current_client = clients[current_index]

            sent = await current_client.send_message(destination_channel, event.message)
            forwarded_messages[message_id] = sent.id
            print(f"[Client {current_index + 1}] Forwarded message ID: {message_id}")

            message_counter += 1

            delay = random.randint(*delay_seconds)
            print(f"Waiting {delay} seconds...")
            await asyncio.sleep(delay)

            if message_counter >= 5:
                message_counter = 0
                current_index = (current_index + 1) % len(clients)
                print(f"Switched to account {current_index + 1}")

        except Exception as e:
            print(f"Error: {e}")

    print("Bot is running...")
    await clients[0].run_until_disconnected()

asyncio.run(main())
