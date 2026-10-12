Aquí tienes el código completo del `README.md` formateado correctamente en un solo bloque continuo, sin espacios extra ni saltos extraños, listo para que lo copies y pegues sin problemas:

```markdown
# Nixis Bot

Un bot de Discord minimalista, seguro y de alto rendimiento diseñado para la monitorizacion e integracion de servidores de Minecraft.

## Descripción

Nixis Bot proporciona monitorizacion en tiempo real del estado de un servidor de Minecraft, ademas de herramientas de administracion minimalistas para gestionar la lista blanca (whitelist) a traves de roles especificos en Discord.

El proyecto esta construido con un enfoque en la simplicidad, evitandose la sobrecarga de datos y priorizando la seguridad de la infraestructura subyacente.

## Características

- Monitorización pasiva de estado del servidor mediante el protocolo Server List Ping.
- Consulta de ip y estado sin exponer puertos de gestion ni servicios criticos.
- Gestion de lista blanca restringida mediante control de acceso basado en roles (RBAC) con IDs unicos.
- Diseno minimalista de respuestas orientadas a la claridad y velocidad.
- Arquitectura basada en variables de entorno para una gestion segura de credenciales.

## Estructura del Proyecto

nixis_bot/
├── main.py            # Punto de entrada principal del bot
├── .env               # Variables de entorno (Token, IP, etc.) [No incluir en repositorio]
├── .gitignore         # Archivo de exclusion de Git
└── README.md          # Documentación del proyecto

## Requisitos Previos

- Python 3.10 o superior
- Una aplicacion registrada en el Portal de Desarrolladores de Discord
- Servidor de Minecraft activo (para consultas de estado)

## Instalación

1. Clona este repositorio en tu maquina local:
   git clone https://github.com/tu-usuario/nixis_bot.git
   cd nixis_bot

2. Crea un entorno virtual e instala las dependencias necesarias:
   python3 -m venv venv
   source venv/bin/activate  # En macOS / Linux
   pip install discord.py mcstatus python-dotenv

3. Crea un archivo `.env` en la raiz del proyecto con el siguiente contenido:
   DISCORD_TOKEN=tu_token_aqui
   SERVER_IP=tu_ip_aqui
   SERVER_PORT=19000

## Uso

Para iniciar el bot en modo local o de desarrollo:

python3 main.py

## Comandos Principales

- `!nixis-status` - Muestra el estado actual y disponibilidad del servidor de Minecraft.
- `!nixis-help` - Lista los comandos disponibles y su sintaxis.
- `!ip` - Muestra la direccion de conexion del servidor.
- `!whitelist <nick>` - Gestiona la entrada de usuarios en la lista blanca (Requiere rol autorizado).

## Seguridad

- El bot implementa verificacion estricta de permisos utilizando IDs de rol unicos para evitar vulnerabilidades de manipulacion de nombres.
- No almacena ni expone tokens de API ni claves privadas en el historial de Git.

```