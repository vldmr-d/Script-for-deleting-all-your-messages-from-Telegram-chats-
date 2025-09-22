#!/usr/bin/python

# -----------------------------------------------------------
# INSTRUCCIONES PARA OBTENER CREDENCIALES (api_id y api_hash)
#
# 1) Abrir: https://my.telegram.org
# 2) Iniciar sesión con el número de teléfono de la cuenta Telegram.
# 3) Ir a "API development tools" y crear una nueva aplicación. 
     #Short name: telethon_delete_message
# 4) Copiar api_id (número) y api_hash (cadena). Guardar con seguridad.
#
# Observaciones de seguridad:
# - No publicar api_hash en repositorios públicos.
# - Si se desea, usar variables de entorno o un fichero .env para guardar
#   las credenciales en lugar de hardcodearlas en el script.
# - Si la cuenta tiene verificación en dos pasos (2FA), el cliente
#   puede pedir la contraseña al iniciar la sesión con Telethon.
# -----------------------------------------------------------

import asyncio
import sys
from telethon import TelegramClient

# Recuerde usar sus propios valores de my.telegram.org
api_id = 12345678  # Sin comillas
api_hash = "xXXxxxXxXxxxxXXxXxx"  # Entre comillas
client = TelegramClient('telethon_delete_message', api_id, api_hash)


async def main():
    # Obtener información del propio usuario
    me = await client.get_me()
    me_id = me.id
    print('{:>14}: {}'.format("Bienvenido", me.username))

    def check_quit():
        input_y = input("¿Continuamos? Escriba 'y' y presione Enter: ")
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
    number_chats = input("Ingrese el número del chat y presione Enter: ")
    print("-" * 80)
    print('Ha seleccionado -->', chat_name[int(number_chats) - 1])
    print("-" * 80)
    check_quit()

    async for messages in client.iter_messages(chat_id[int(number_chats) - 1],
                                               from_user=me_id, limit=3000):
        await asyncio.sleep(1)
        count_messages += 1
        if messages.text:
            print('{:>10} Eliminado --> {}'.format(count_messages, messages.date), messages.text[:48])
            await client.delete_messages(chat_id[int(number_chats) - 1], messages.id)
        else:
            print('{:>10} Eliminado --> {}'.format(count_messages, messages.date), "Algún archivo multimedia (foto, video, audio)")
            await client.delete_messages(chat_id[int(number_chats) - 1], messages.id)


with client:
    client.loop.run_until_complete(main())

print("-" * 80)
print("¡Felicidades, ha eliminado todo!")

