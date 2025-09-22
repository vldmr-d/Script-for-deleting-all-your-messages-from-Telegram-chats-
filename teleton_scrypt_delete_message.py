#!/usr/bin/python

# -----------------------------------------------------------
# ІНСТРУКЦІЯ ДЛЯ ОТРИМАННЯ ОБЛІКОВИХ ДАНИХ (api_id та api_hash)
#
# 1) Відкрити: https://my.telegram.org
# 2) Увійти, використовуючи номер телефону акаунта Telegram.
# 3) Перейти до "API development tools" і створити новий застосунок. 
#    Short name: telethon_delete_message
# 4) Скопіювати api_id (число) та api_hash (рядок). Зберегти у безпечному місці.
#
# Зауваження щодо безпеки:
# - Не публікувати api_hash у публічних репозиторіях.
# - За потреби використати змінні середовища або файл .env для збереження
#   облікових даних замість прописування їх у коді.
# - Якщо в акаунті увімкнено двофакторну автентифікацію (2FA),
#   клієнт може запитати пароль під час входу в Telethon.
# -----------------------------------------------------------

import asyncio
import sys
from telethon import TelegramClient

# Використайте власні значення з my.telegram.org
api_id = 12345678  # Без лапок
api_hash = "xXXxxxXxXxxxxXXxXxx"  # У лапках
client = TelegramClient('telethon_delete_message', api_id, api_hash)


async def main():
    # Отримати інформацію про власний акаунт
    me = await client.get_me()
    me_id = me.id
    print('{:>14}: {}'.format("Вітаю", me.username))

    def check_quit():
        input_y = input("Продовжимо? Введіть 'y' і натисніть Enter: ")
        if input_y != 'y':
            sys.exit(0)

    check_quit()
    chat_name = []
    chat_id = []

    count_chats = 0
    async for dialog in client.iter_dialogs():
        await asyncio.sleep(0.25)
        count_chats += 1
        chat_name.append(dialog.title)
        chat_id.append(dialog.id)
        print('{:>14}: {}'.format(count_chats, dialog.title), dialog.id)

    count_messages = 0
    print("-" * 80)
    number_chats = input("Введіть номер чату й натисніть Enter: ")
    print("-" * 80)
    print('Ви обрали -->', chat_name[int(number_chats) - 1])
    print("-" * 80)
    check_quit()

    async for messages in client.iter_messages(chat_id[int(number_chats) - 1],
                                               from_user=me_id, limit=3000):
        await asyncio.sleep(1)
        count_messages += 1
        if messages.text:
            print('{:>10} Видалено --> {}'.format(count_messages, messages.date), messages.text[:48])
            await client.delete_messages(chat_id[int(number_chats) - 1], messages.id)
        else:
            print('{:>10} Видалено --> {}'.format(count_messages, messages.date), "Мультимедійний файл (фото, відео, аудіо)")
            await client.delete_messages(chat_id[int(number_chats) - 1], messages.id)


with client:
    client.loop.run_until_complete(main())

print("-" * 80)
print("Вітаємо, усі ваші повідомлення було видалено!")
