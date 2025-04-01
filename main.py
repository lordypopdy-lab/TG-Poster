from telethon import TelegramClient, events

api_id = 14458814
api_hash = "b1e1a2ffd6000df2ea7b40517523bbbb"

source_channel = "xmcryptonews"
destination_channel = "@BitclubChatGroup"

client = TelegramClient("poster_session", api_id, api_hash)

processed_messages = set()

@client.on(events.NewMessage(chats=source_channel))
async def forward_message(event):
    try:
        message_id = event.message.id
        if message_id not in processed_messages:
            processed_messages.add(message_id)
            await client.send_message(destination_channel, event.message)
    except Exception as e:
        print(f"Error forwarding message: {e}")

client.start()
print("Bot is running...")
client.run_until_disconnected()
