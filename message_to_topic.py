from telethon import TelegramClient, events
from config import api_id, api_hash, TARGET_CHAT, TARGET_TOPIC_ID, SOURCE_CHANNELS



client = TelegramClient("my_account", api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    try:
        msg = event.message

        if msg.text:
            await client.send_message(
                entity=TARGET_CHAT,
                message=msg.text,
                reply_to=TARGET_TOPIC_ID
            )

        elif msg.media:
            await client.send_file(
                entity=TARGET_CHAT,
                file=msg.media,
                caption=msg.text if msg.text else "",
                reply_to=TARGET_TOPIC_ID
            )

    except Exception as e:
        print("Ошибка при пересылке:", e)

with client:
    print("Бот запущен, слушаю каналы...")
    client.run_until_disconnected()
