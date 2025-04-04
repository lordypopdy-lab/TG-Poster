# from telethon import TelegramClient, events

# api_id = 14458814
# api_hash = "b1e1a2ffd6000df2ea7b40517523bbbb"

# source_channel = "xmcryptonews"
# destination_channel = "@BitclubChatGroup"

# client = TelegramClient("poster_session", api_id, api_hash)

# processed_messages = set()

# @client.on(events.NewMessage(chats=source_channel))
# async def forward_message(event):
#     try:
#         message_id = event.message.id
#         if message_id not in processed_messages:
#             processed_messages.add(message_id)
#             await client.send_message(destination_channel, event.message)
#     except Exception as e:
#         print(f"Error forwarding message: {e}")

# client.start()
# print("Bot is running...")
# client.run_until_disconnected()



from telethon import TelegramClient, events
from datetime import datetime, timedelta

api_id = 14458814
api_hash = "b1e1a2ffd6000df2ea7b40517523bbbb"

source_channel = "xmcryptonews"
destination_channel = "@BitclubChatGroup"

client = TelegramClient("poster_session", api_id, api_hash)

# In-memory store of forwarded message IDs and their destination message ID
forwarded_messages = {}

@client.on(events.NewMessage(chats=source_channel))
async def forward_message(event):
    try:
        message_id = event.message.id
        message_text = event.message.message or ""

        # If the message was already forwarded
        if message_id in forwarded_messages:
            # Delete the previous one
            old_message = forwarded_messages[message_id]
            await client.delete_messages(destination_channel, old_message)
            print(f"Deleted duplicate message: {message_id}")

        # Forward the new message
        sent = await client.send_message(destination_channel, event.message)
        forwarded_messages[message_id] = sent.id
        print(f"Forwarded message: {message_id}")

    except Exception as e:
        print(f"Error forwarding/deleting message: {e}")

client.start()
print("Bot is running...")
client.run_until_disconnected()
