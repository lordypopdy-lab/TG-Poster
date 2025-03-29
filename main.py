from telethon import TelegramClient, events

# Your API credentials (Get from https://my.telegram.org/apps)
api_id = "14458814"
api_hash = "b1e1a2ffd6000df2ea7b40517523bbbb"

# Source and destination channels
source_channel = "xmcryptonews"
destination_channel = "@BitclubChatGroup"

# Initialize the Telegram Client
client = TelegramClient("poster_session", api_id, api_hash)

# Function to copy messages
@client.on(events.NewMessage(chats=source_channel))
async def forward_message(event):
    await client.send_message(destination_channel, event.message)

# Start the client
client.start()
print("Bot is running...")
client.run_until_disconnected()
