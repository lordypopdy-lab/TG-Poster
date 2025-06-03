from telethon import TelegramClient, events
import asyncio

# Replace with your values
api_id = 123456            # your api_id from https://my.telegram.org
api_hash = 'your_api_hash' # your api_hash from https://my.telegram.org

# Replace with actual usernames or IDs
source_channel = '@xmcryptonews'   # e.g. 'cryptoalerts' or -1001234567890
target_channel = '@BitclubCryptoNews'   # e.g. 'mypublicchannel' or -1009876543210

client = TelegramClient('poster001', api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def forward_handler(event):
    try:
        await client.forward_messages(target_channel, event.message)
        print(f"Forwarded message ID {event.message.id}")
    except Exception as e:
        print(f"Error forwarding message: {e}")

async def main():
    await client.start()
    print("Client started. Listening for new messages...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
    
