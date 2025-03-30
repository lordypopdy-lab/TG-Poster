from telethon import TelegramClient, events

# Your API credentials (Get from https://my.telegram.org/apps)
api_id = 14458814
api_hash = "b1e1a2ffd6000df2ea7b40517523bbbb"

# Source and destination channels
source_channel = "xmcryptonews"
destination_channel = "@BitclubChatGroup"

# Initialize the Telegram Client
client = TelegramClient("poster_session", api_id, api_hash)

# Set to store processed message IDs
processed_messages = set()

# Function to copy messages (avoiding duplicates)
@client.on(events.NewMessage(chats=source_channel))
async def forward_message(event):
    message_id = event.message.id  # Unique ID of the message
    if message_id not in processed_messages:  # Check if already processed
        processed_messages.add(message_id)  # Mark as processed
        await client.send_message(destination_channel, event.message)

# Start the client
client.start()
print("Bot is running...")
client.run_until_disconnected()
