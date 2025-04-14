from telethon import TelegramClient, events
import asyncio
import random
import os

api_id = 14458814
api_hash = "b1e1a2ffd6000df2ea7b40517523bbbb"

source_channel_username = "@xmcryptonews"
destination_channel = "@BitclubChatGroup"

session_names = ["poster_session1", "poster_session2", "poster_session3"]
clients = []
message_counter = 0
current_index = 0
delay_seconds = (10, 12)
forwarded_messages = {}

async def main():
    global message_counter, current_index

    for session in session_names:
        try:
            session_path = os.path.join(os.getcwd(), session)
            client = TelegramClient(session_path, api_id, api_hash)

            await client.connect()

            if not await client.is_user_authorized():
                print(f"❌ Session not authorized: {session}")
                continue

            clients.append(client)
            print(f"✅ Loaded session: {session}")

        except Exception as e:
            print(f"⚠️ Error with session {session}: {e}")

    if not clients:
        print("❌ No valid clients available.")
        return

    # Get channel entity (once)
    source_entity = await clients[0].get_entity(source_channel_username)

    @clients[0].on(events.NewMessage(chats=source_entity))
    async def handler(event):
        global message_counter, current_index

        try:
            message_id = event.message.id

            if message_id in forwarded_messages:
                return

            current_client = clients[current_index]

            sent = await current_client.send_message(destination_channel, event.message)
            forwarded_messages[message_id] = sent.id
            print(f"[Client {current_index + 1}] ➤ Forwarded message ID: {message_id}")

            message_counter += 1

            delay = random.randint(*delay_seconds)
            print(f"⏳ Waiting {delay} seconds...")
            await asyncio.sleep(delay)

            if message_counter >= 5:
                message_counter = 0
                current_index = (current_index + 1) % len(clients)
                print(f"🔁 Switched to account {current_index + 1}")

        except Exception as e:
            print(f"⚠️ Handler error: {e}")

    print("🚀 Bot running on server...")
    await clients[0].run_until_disconnected()

asyncio.run(main())
