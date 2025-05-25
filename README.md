
from pathlib import Path

# Contenido actualizado del README.md
readme_content = """
# 🤖 Bot Autopublicador para Telegram

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/Wito50/Bot_Autopublicador)

Bot automatizado para publicar mensajes en grupos/channels de Telegram, desarrollado con Python y Telethon.

## 🔐 Requisitos de configuración
Antes de comenzar, necesitarás:
- API ID y Hash de [my.telegram.org](https://my.telegram.org/auth)
- Token del bot (obtenido con [@BotFather](https://t.me/BotFather))
- ID de tu grupo (debe comenzar con `-100`)
- Tu ID de usuario (consúltalo con [@userinfobot](https://t.me/userinfobot))

## 🛠 Instalación local
```bash
git clone https://github.com/Wito50/Bot_Autopublicador.git
cd Bot_Autopublicador
pip install -r requirements.txt
```

## ⚙ Configuración
Crea un archivo `.env` en la raíz del proyecto con:
```ini
API_ID=12345678
API_HASH=tu_api_hash_telegram
BOT_TOKEN=tu_token_de_bot
GRUPO_ID=-1001234567890
ADMIN_ID=1234567890
```

## 🚀 Despliegue en Railway
1. Haz clic en [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/Wito50/Bot_Autopublicador)
2. Completa las variables de entorno con tus credenciales
3. ¡Listo! El bot se desplegará automáticamente

## 📋 Comandos disponibles
| Comando | Uso | Descripción |
|---------|-----|-------------|
| `/nuevo [ID]` | `/nuevo 1` | Crea nueva publicación |
| `/mensaje [ID] [texto]` | `/mensaje 1 Hola mundo` | Define texto |
| `/imagen [ID]` | Responde a una imagen con `/imagen 1` | Añade imagen |
| `/frecuencia [ID] [segundos]` | `/frecuencia 1 3600` | Establece intervalo |
| `/duracion [ID] [segundos]` | `/duracion 1 86400` | Define cuánto tiempo publicar |
| `/empezar [ID]` | `/empezar 1` | Inicia publicación |
| `/parar [ID]` | `/parar 1` | Detiene publicación |
| `/estado` | `/estado` | Muestra configuración actual |
| `/listar` | `/listar` | Muestra todas las publicaciones configuradas |

## 🛡 Seguridad
- Nunca compartas tu `BOT_TOKEN` o `API_HASH`
- Usa variables de entorno (nunca las incluyas en el código)
- Si expusiste accidentalmente tus credenciales, regenera el token con @BotFather

## 📄 Licencia
MIT © [Wito50](https://github.com/Wito50)
"""

# Guardar archivo README.md
readme_path = Path("/mnt/data/README.md")
readme_path.write_text(readme_content.strip())

readme_path
