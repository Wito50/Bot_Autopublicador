import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient, events

# Cargar variables de entorno
load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
grupo_id = int(os.getenv('GRUPO_ID'))
admin_id = int(os.getenv('ADMIN_ID'))

# Inicializar cliente
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# Diccionario para múltiples mensajes
mensajes = {}

# Función para autopublicar
async def autopublicar(index):
    while mensajes[index]['activo']:
        mensaje = mensajes[index]['mensaje']
        file_id = mensajes[index]['file_id']
        try:
            if file_id:
                await client.send_file(grupo_id, file_id, caption=mensaje)
            else:
                await client.send_message(grupo_id, mensaje)
            print(f"[LOG] Mensaje {index} enviado a las {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"[ERROR] Error al enviar mensaje {index}: {e}")
        await asyncio.sleep(mensajes[index]['frecuencia'])

# Comando para crear nuevo mensaje
@client.on(events.NewMessage(pattern=r'/nuevo (\d+)', from_users=admin_id))
async def nuevo_handler(event):
    index = int(event.pattern_match.group(1))
    mensajes[index] = {
        'mensaje': 'Mensaje por defecto',
        'file_id': None,
        'frecuencia': 60,
        'duracion': 86400,
        'activo': False,
        'tarea': None
    }
    print(f"[LOG] Nuevo mensaje {index} creado.")
    await event.respond(f'Mensaje {index} creado.')

# Comando para definir el texto
@client.on(events.NewMessage(pattern=r'/mensaje (\d+) (.+)', from_users=admin_id))
async def mensaje_handler(event):
    index = int(event.pattern_match.group(1))
    texto = event.pattern_match.group(2)
    if index in mensajes:
        mensajes[index]['mensaje'] = texto
        print(f"[LOG] Texto actualizado para mensaje {index}.")
        await event.respond(f'Mensaje {index} actualizado.')
    else:
        await event.respond('Primero crea el mensaje con /nuevo.')

# Comando para definir la imagen (CORREGIDO)
@client.on(events.NewMessage(pattern=r'/imagen (\d+)', from_users=admin_id))
async def imagen_handler(event):
    index = int(event.pattern_match.group(1))
    media = event.message.media

    if index in mensajes and media:
        try:
            mensajes[index]['file_id'] = media
            print(f"[LOG] Imagen añadida a mensaje {index}.")
            await event.respond(f'Imagen asignada a mensaje {index}.')
        except Exception as e:
            print(f"[ERROR] al capturar file_id: {e}")
            await event.respond('Error al capturar la imagen.')
    else:
        await event.respond('Primero crea el mensaje con /nuevo o responde a una imagen.')

# Comando para establecer frecuencia
@client.on(events.NewMessage(pattern=r'/frecuencia (\d+) (\d+)', from_users=admin_id))
async def frecuencia_handler(event):
    index = int(event.pattern_match.group(1))
    freq = int(event.pattern_match.group(2))
    if index in mensajes:
        mensajes[index]['frecuencia'] = freq
        print(f"[LOG] Frecuencia del mensaje {index} actualizada a {freq} segundos.")
        await event.respond(f'Frecuencia de mensaje {index} actualizada a {freq} segundos.')
    else:
        await event.respond('Primero crea el mensaje con /nuevo.')

# Comando para establecer duración
@client.on(events.NewMessage(pattern=r'/duracion (\d+) (\d+)', from_users=admin_id))
async def duracion_handler(event):
    index = int(event.pattern_match.group(1))
    dur = int(event.pattern_match.group(2))
    if index in mensajes:
        mensajes[index]['duracion'] = dur
        print(f"[LOG] Duración del mensaje {index} actualizada a {dur} segundos.")
        await event.respond(f'Duración de mensaje {index} actualizada a {dur} segundos.')
    else:
        await event.respond('Primero crea el mensaje con /nuevo.')

# Comando para iniciar publicación
@client.on(events.NewMessage(pattern=r'/empezar (\d+)', from_users=admin_id))
async def empezar_handler(event):
    index = int(event.pattern_match.group(1))
    if index in mensajes and not mensajes[index]['activo']:
        mensajes[index]['activo'] = True
        mensajes[index]['tarea'] = asyncio.create_task(autopublicar(index))

        async def detener():
            await asyncio.sleep(mensajes[index]['duracion'])
            mensajes[index]['activo'] = False
            if mensajes[index]['tarea']:
                mensajes[index]['tarea'].cancel()
            print(f"[LOG] Publicación del mensaje {index} detenida automáticamente por duración.")

        asyncio.create_task(detener())
        print(f"[LOG] Publicación del mensaje {index} iniciada.")
        await event.respond(f'Mensaje {index} comenzado.')
    else:
        await event.respond('Primero crea el mensaje con /nuevo o ya está activo.')

# Comando para detener publicación
@client.on(events.NewMessage(pattern=r'/parar (\d+)', from_users=admin_id))
async def parar_handler(event):
    index = int(event.pattern_match.group(1))
    if index in mensajes:
        mensajes[index]['activo'] = False
        if mensajes[index]['tarea']:
            mensajes[index]['tarea'].cancel()
        print(f"[LOG] Publicación del mensaje {index} detenida por comando.")
        await event.respond(f'Mensaje {index} detenido.')
    else:
        await event.respond('Primero crea el mensaje con /nuevo.')

# Comando para mostrar estado
@client.on(events.NewMessage(pattern=r'/estado', from_users=admin_id))
async def estado_handler(event):
    estado_texto = ''
    for i, msg in mensajes.items():
        estado_texto += (
            f'\nMensaje {i}:\n'
            f'- Activo: {msg["activo"]}\n'
            f'- Frecuencia: {msg["frecuencia"]}s\n'
            f'- Duración: {msg["duracion"]}s\n'
            f'- Texto: {msg["mensaje"]}\n'
            f'- Imagen: {"Sí" if msg["file_id"] else "No"}\n'
        )
    print("[LOG] Estado consultado.")
    if estado_texto:
        await event.respond(estado_texto)
    else:
        await event.respond('No hay mensajes configurados.')

# Ejecutar el bot
print("[LOG] Bot en marcha...")
client.run_until_disconnected()
