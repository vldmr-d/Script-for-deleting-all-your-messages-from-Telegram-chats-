from telethon import TelegramClient
import asyncio
import sys

# Remember to use your own values from my.telegram.org!
api_id = xxxxxxxxxxx  # Без кавычек
api_hash = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # В кавычках
client = TelegramClient('telethon_delete_message', api_id, api_hash)


async def main():
    # Getting information about yourself
    me = await client.get_me()
    me_id = me.id
    print('{:>14}: {}'.format("Здравствуй", me.username))

    def check_quit():
        input_y = input("Продолжим? Введите 'y' и нажмите Enter: ")
        if input_y == 'y':
            pass
        else:
            sys.exit(0)

    check_quit()
    chat_name = []
    chat_id = []

    count_chats = 0
    async for dialog in client.iter_dialogs():
        await asyncio.sleep(0.25)
        count_chats = count_chats + 1
        chat_name.append(dialog.title)
        chat_id.append(dialog.id)
        print('{:>14}: {}'.format(count_chats, dialog.title), dialog.id)

    count_messages = 0
    print("-" * 80)
    number_chats = input("Введите 'номер' чата и нажмите Enter: ")
    print("-" * 80)
    print('Вы выбрали -->', chat_name[int(number_chats) - 1])
    print("-" * 80)
    check_quit()

    async for messages in client.iter_messages(chat_id[int(number_chats) - 1],
                                               from_user=me_id, limit=3000, wait_time=60):
        await asyncio.sleep(1)
        count_messages = count_messages + 1
        if messages.text is not None:
            if messages.text:
                print('{:>10} Удалено --> {}'.format(count_messages, messages.date), messages.text[:48])
                await client.delete_messages(chat_id[int(number_chats) - 1], messages.id)
            else:
                print('{:>10} Удалено --> {}'.format(count_messages, messages.date), 'Какое-то Фото, Видео или Аудио')
                await client.delete_messages(chat_id[int(number_chats) - 1], messages.id)


with client:
    client.loop.run_until_complete(main())

print("-" * 80)
print("Поздравляю вы всё удалили!")
