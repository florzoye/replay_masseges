from telethon import TelegramClient, events
from config import api_id, api_hash, TARGET_CHAT, TARGET_TOPIC_ID, SOURCE_CHANNELS


client = TelegramClient("my_account", api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    try:
        msg = event.message
        chat = await event.get_chat()   # получаем объект канала/чата
        channel_name = chat.title if hasattr(chat, "title") else "Неизвестный канал"

        prefix = f"📩 Переслано от: {channel_name}\n\n"

        if msg.text:
            await client.send_message(
                entity=TARGET_CHAT,
                message=prefix + msg.text,
                reply_to=TARGET_TOPIC_ID
            )

        elif msg.media:
            await client.send_file(
                entity=TARGET_CHAT,
                file=msg.media,
                caption=prefix + (msg.text if msg.text else ""),
                reply_to=TARGET_TOPIC_ID
            )

    except Exception as e:
        print("Ошибка при пересылке:", e)


with client:
    print("Бот запущен, слушаю каналы...")
    client.run_until_disconnected()
