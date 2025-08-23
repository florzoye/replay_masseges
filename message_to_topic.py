from telethon import TelegramClient, events
from config import api_id, api_hash, TARGET_CHAT, TARGET_TOPIC_ID, SOURCE_CHANNELS


client = TelegramClient("my_account", api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    try:
        msg = event.message
        chat = await event.get_chat()
        channel_name = chat.title if hasattr(chat, "title") else "Неизвестный канал"
        
        prefix = f"📩 Переслано от: {channel_name}\n\n"
        
        # Получаем весь текст (включая подпись к медиа)
        full_text = ""
        if msg.text:
            full_text = msg.text
        elif msg.message:  # подпись к медиафайлу
            full_text = msg.message
            
        # Если есть медиафайл - отправляем его с текстом
        if msg.media:
            await client.send_file(
                entity=TARGET_CHAT,
                file=msg.media,
                caption=prefix + full_text if full_text else prefix + "Медиафайл без подписи",
                reply_to=TARGET_TOPIC_ID
            )
        # Если только текст - отправляем текст
        elif full_text:
            await client.send_message(
                entity=TARGET_CHAT,
                message=prefix + full_text,
                reply_to=TARGET_TOPIC_ID
            )
        # Если вообще нет контента (например, только стикер без подписи)
        else:
            await client.send_message(
                entity=TARGET_CHAT,
                message=prefix + "Сообщение без текста",
                reply_to=TARGET_TOPIC_ID
            )
            
    except Exception as e:
        print("Ошибка при пересылке:", e)

with client:
    print("Бот запущен, слушаю каналы...")
    client.run_until_disconnected()
