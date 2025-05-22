import asyncio
import os
from datetime import datetime
from telethon import TelegramClient, events

# Configuración
api_id = 28231389
api_hash = '9d0dbb88eb4216565c5280a22788cbf9'
bot_token = '7594650445:AAGuSGGzaQ2V3LVb7d_yUjyDW5ze0rYKUbk'
grupo_id = -1002544036731
admin_id = 933399068  # Tu ID personal

# Inicializar cliente
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# Diccionario para múltiples mensajes
mensajes = {}

# Función para autopublicar
async def autopublicar(index):
    while mensajes[index]['activo']:
        mensaje = mensajes[index]['mensaje']
        imagen = mensajes[index]['imagen']
        try:
            if imagen and os.path.exists(imagen):
                await client.send_file(grupo_id, imagen, caption=mensaje)
            else:
                await client.send_message(grupo_id, mensaje)
            print(f"Mensaje {index} enviado a las {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"Error al enviar mensaje {index}: {e}")
        await asyncio.sleep(mensajes[index]['frecuencia'])

# Comando para crear nuevo mensaje
@client.on(events.NewMessage(pattern=r'/nuevo (\d+)', from_users=admin_id))
async def nuevo_handler(event):
    index = int(event.pattern_match.group(1))
    mensajes[index] = {
        'mensaje': 'Mensaje por defecto',
        'imagen': None,
        'frecuencia': 60,
        'duracion': 86400,
        'activo': False,
        'tarea': None
    }
    await event.respond(f'Mensaje {index} creado.')

# Comando para definir el texto
@client.on(events.NewMessage(pattern=r'/mensaje (\d+) (.+)', from_users=admin_id))
async def mensaje_handler(event):
    index = int(event.pattern_match.group(1))
    texto = event.pattern_match.group(2)
    if index in mensajes:
        mensajes[index]['mensaje'] = texto
        await event.respond(f'Mensaje {index} actualizado.')
    else:
        await event.respond('Primero crea el mensaje con /nuevo.')

# Comando para definir la imagen
async def autopublicar(index):
    while mensajes[index]['activo']:
        mensaje = mensajes[index]['mensaje']
        file_id = mensajes[index]['file_id']  # Usa file_id en lugar de ruta local
        try:
            if file_id:
                await client.send_file(grupo_id, file_id, caption=mensaje)
            else:
                await client.send_message(grupo_id, mensaje)
            print(f"Mensaje {index} enviado a las {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"Error al enviar mensaje {index}: {e}")
        await asyncio.sleep(mensajes[index]['frecuencia'])

# Comando para establecer frecuencia
@client.on(events.NewMessage(pattern=r'/frecuencia (\d+) (\d+)', from_users=admin_id))
async def frecuencia_handler(event):
    index = int(event.pattern_match.group(1))
    freq = int(event.pattern_match.group(2))
    if index in mensajes:
        mensajes[index]['frecuencia'] = freq
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

        asyncio.create_task(detener())
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
        await event.respond(f'Mensaje {index} detenido.')
    else:
        await event.respond('Primero crea el mensaje con /nuevo.')

# Comando para mostrar estado
@client.on(events.NewMessage(pattern=r'/estado', from_users=admin_id))
async def estado_handler(event):
    estado_texto = ''
    for i, msg in mensajes.items():
        estado_texto += f'\nMensaje {i}:\n- Activo: {msg["activo"]}\n- Frecuencia: {msg["frecuencia"]}s\n- Duración: {msg["duracion"]}s\n- Texto: {msg["mensaje"]}\n- Imagen: {msg["imagen"]}\n'
    if estado_texto:
        await event.respond(estado_texto)
    else:
        await event.respond('No hay mensajes configurados.')

# Ejecutar el bot
print("Bot en marcha...")
client.run_until_disconnected()
