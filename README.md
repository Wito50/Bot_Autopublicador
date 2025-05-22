
# 🤖  Bot_Autopublicador

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/tuusuario/turepo&envs=API_ID,API_HASH,BOT_TOKEN,GRUPO_ID,ADMIN_ID)

Bot de Telegram para publicar mensajes automáticos en grupos, desarrollado con Python y la librería Telethon.

## 🚀 Características

- ✅ Publicación programada de mensajes/imágenes
- ✅ Multiples mensajes configurables
- ✅ Comandos de administrador fáciles de usar
- ✅ Despliegue sencillo en Railway.app

## 📦 Requisitos

- Python 3.8+
- Cuenta de [Telegram](https://telegram.org)
- Credenciales de [API de Telegram](https://my.telegram.org/auth)

## 🛠️ Instalación local

1. Clona el repositorio:
```bash
git clone https://github.com/tuusuario/turepo.git
cd turepo
```

2. Instala dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
```bash
export API_ID=tu_api_id
export API_HASH=tu_api_hash
export BOT_TOKEN=tu_token_bot
export GRUPO_ID=tu_id_grupo
export ADMIN_ID=tu_id_admin
```

4. Ejecuta el bot:
```bash
python main.py
```

## 🖥️ Comandos disponibles

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/nuevo [ID]` | Crea un nuevo mensaje | `/nuevo 1` |
| `/mensaje [ID] [texto]` | Define el texto | `/mensaje 1 Hola mundo` |
| `/imagen [ID]` | Añade imagen (responder a foto) | `/imagen 1` |
| `/frecuencia [ID] [segundos]` | Establece intervalo | `/frecuencia 1 3600` |
| `/empezar [ID]` | Inicia publicación | `/empezar 1` |
| `/parar [ID]` | Detiene publicación | `/parar 1` |
| `/estado` | Muestra configuración | `/estado` |

## ☁️ Despliegue en Railway

1. Haz clic en el botón [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/tuusuario/turepo&envs=API_ID,API_HASH,BOT_TOKEN,GRUPO_ID,ADMIN_ID)
2. Completa las variables de entorno:
   - `API_ID`
   - `API_HASH`
   - `BOT_TOKEN`
   - `GRUPO_ID`
   - `ADMIN_ID`
3. ¡Listo! El bot se desplegará automáticamente.

## 📝 Notas importantes

- Para imágenes: responde con `/imagen [ID]` a una foto que hayas enviado al bot.
- Los IDs de grupo deben comenzar con `-100` (supergrupos).
- En Railway, revisa los logs si hay errores.

## 🤝 Contribuir

Si deseas mejorar este proyecto:
1. Haz fork del repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcion`)
3. Haz commit de tus cambios (`git commit -am 'Añade nueva función'`)
4. Haz push a la rama (`git push origin feature/nueva-funcion`)
5. Abre un Pull Request

## 📄 Licencia

MIT © [Wito50](https://github.com/Wito50)
