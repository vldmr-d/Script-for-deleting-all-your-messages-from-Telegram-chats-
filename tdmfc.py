from time import sleep
from pyrogram import Client

"""
Получение api_id

Чтобы получить идентификатор API и разработать собственное приложение с помощью API Telegram,
 вам необходимо сделать следующее:

     Зарегистрируйтесь в Telegram с помощью любого приложения.
     Войдите в свое ядро Telegram: https://my.telegram.org.
     Перейдите в «Инструменты разработки API» и заполните форму.
     Вы получите базовые адреса, а также параметры api_id и api_hash, необходимые для авторизации пользователя.
     На данный момент к каждому номеру может быть подключен только один api_id.

Мы будем отправлять важные уведомления разработчикам на номер телефона, который вы используете в этом процессе,
 поэтому используйте актуальный номер, связанный с вашей активной учетной записью Telegram. 
"""
app = Client(
    #"telegram_delete_message",  # название этой программы в конфигурационном файле в директории откуда запускаете скрипт
    "my_account",
    api_id="xxxxxxxxxxx",  # ваш api_id в кавічках
    api_hash="xxxxxxxxxxxxxxxxxxxxxxxx"  # ваш api_hash в кавычках
)

list_chats = []
name_chats = []

with app:
    me = app.get_me()
    print("Ваш id", me.id)
    count_chats = 0
    for dialog in app.get_dialogs(limit=100, offset_date=0):
        count_chats = count_chats + 1
        list_chats.append(dialog.chat.id)
        name_chats.append(dialog.chat.title)
        print(count_chats, "id_chats=", dialog.chat.id, dialog.chat.type, dialog.chat.title, dialog.chat.first_name)
    print("Данный скрипт удаляет по 300 сообщений за раз,"
          " если больше сообщений, запустите этот скрипт еще раз")
    select_chat = input("Поставьте номер выбраного чата : ")
    id_chats = list_chats[int(select_chat) - 1]
    print("Вы выбрали", id_chats, name_chats[int(select_chat) - 1])
    while input("Нажмите 'y' если хотите продолжить: ") == "y":
        print("Чтобы прервать скрипт нажмите CTR + C")
        for message in app.search_messages(chat_id=id_chats, limit=300, from_user=me.id):
            sleep(1)
            app.delete_messages(id_chats, message.message_id)
            print(message.message_id, message.text, message.media, " <-- Удалено!")
        else:
            break

