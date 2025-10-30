from telethon.sync import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.errors import FloodWaitError
import asyncio

# ===== EDIT YE (API keys) =====
api_id = 1234567  # Your number
api_hash = '872gwy7y22yui28922228y699gegh21'  # With quotes
phone = '+91XXXXXXXXXX'  # Your phone
# ==============================

description = 'Auto-created group from text file! Welcome.'  # Change if want

async def create_groups():
    # Load names from text file
    try:
        with open('group_names.txt', 'r', encoding='utf-8') as file:
            group_names = [line.strip() for line in file if line.strip()]  # Read lines, ignore empty
        print(f'📄 Loaded {len(group_names)} group names from file!')
    except FileNotFoundError:
        print('❌ group_names.txt not found! Create it with names (one per line).')
        return

    client = TelegramClient('session', api_id, api_hash)
    await client.start(phone=phone)  # Enter code if first time

    print('🚀 Starting creation... (Using channel method)')
    count = 0

    for name in group_names:
        try:
            result = await client(CreateChannelRequest(
                title=name,
                about=description,
                megagroup=True  # Supergroup (like normal group)
            ))
            chat = result.chats
            print(f'✅ {name} created! ID: {chat.id}')
            count += 1
            await asyncio.sleep(5)  # Wait

        except FloodWaitError as e:
            print(f'⚠️ Wait {e.seconds}s...')
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f'❌ Error {name}: {e}')

    await client.disconnect()
    print(f'🎉 {count}/{len(group_names)} groups done! Check Telegram.')

if __name__ == '__main__':
    asyncio.run(create_groups())

