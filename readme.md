# Nixis Bot

Motor de bot de Discord minimalista y modular para la monitorizacion e integracion de servidores de Minecraft.

## Descripcion

Nixis Bot esta disenado como una base limpia y ligera. Proporciona comandos esenciales y monitorizacion pasiva mediante Server List Ping, permitiendo extender la funcionalidad con sistemas propios (como la gestion de whitelist) segun las necesidades de cada infraestructura.

## Caracteristicas

- Monitorizacion pasiva del estado del servidor.
- Estructura modular basada en extensiones de Discord.py.
- Configuracion mediante variables de entorno (.env).
- Codigo limpio y directo, sin dependencias innecesarias.

## Estructura del Proyecto

nixis_bot/
├── main.py            # Punto de entrada principal
├── .env               # Variables de entorno locales [Ignorado por Git]
├── .gitignore         # Archivos excluidos del control de versiones
└── README.md          # Documentacion del proyecto

## Instalacion y Puesta en Marcha

1. Clona el repositorio:
   git clone https://github.com/tu-usuario/nixis_bot.git
   cd nixis_bot

2. Configura tu entorno virtual e instala las dependencias:
   python3 -m venv venv
   source venv/bin/activate
   pip install discord.py mcstatus python-dotenv

3. Crea tu propio archivo `.env` basado en la configuracion de tu entorno:
   DISCORD_TOKEN=tu_token_aqui
   SERVER_IP=tu_ip_aqui
   SERVER_PORT=tu_puerto_aqui

4. Ejecuta el motor:
   python3 main.py

## Comandos Base

- `!nixis-status` - Comprueba el estado actual del servidor configurado.
- `!nixis-help` - Muestra la lista de comandos disponibles.
- `!ip` - Muestra la direccion de conexion del servidor.