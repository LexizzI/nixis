from dotenv import load_dotenv
from mcstatus import JavaServer
from discord.ext import commands
from discord.ext import tasks
from mcrcon import MCRcon
import discord
import os

# Carga y verificacion de variables de entorno

load_dotenv()

bot_token = os.getenv("DISCORD_SK")
mc_ip = os.getenv("MC_SERVER_IP")
mc_port = os.getenv("MC_SERVER_PORT")
servername = os.getenv("MC_SERVER_NAME")
rcon = os.getenv("RCON_PORT")
rcon_pswd = os.getenv("RCON_PSWD")

if not mc_ip or not mc_port:
    print("ERROR!: No se ha definido una ip y puerto de minecraft server en el .env")
else:
    print(f"INFO: Definida la ip del server correctamente!")

if bot_token is None:
    print("ERROR!: No se ha encontrado ninguna token de discord en el .env")
    raise SystemExit



intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)

# Loop de RPC

@tasks.loop(seconds=5)
async def rpc_update():
    try:
        server = await JavaServer.async_lookup(f"{mc_ip}:{mc_port}")
        status = await server.async_status()
        
        presence_text = f"{servername} [{status.players.online}/{status.players.max}] - En linea!"
        
        await bot.change_presence(activity=discord.Game(name=presence_text))
        
    except Exception:
        await bot.change_presence(activity=discord.Game(name="Selunecraft [offline]"))


@bot.event
async def on_ready():
    rpc_update.start()
    print(f"Hola! Soy {bot.user.name}, todos los parametros correctos, lista para funcionar!")



def send_rcon_command(command: str) -> str:
    try:

        if not mc_ip or not rcon or not rcon_pswd:
            return "ERROR: Faltan variables de RCON en el .env"
        with MCRcon(mc_ip, rcon_pswd, int(rcon)) as mcr:
            return mcr.command(command)
    
    except Exception as exc:
        print(f"ERROR: No se pudo ejecutar el comando de RCON: {exc}")
        return f"ERROR: {exc}"


    

# bloque con las funciones de los comandos

@bot.command(name="nixis-help")
async def help(ctx):
    print(f"INFO: El usuario {ctx.author} ha solicitado el comando de ayuda")
    await ctx.send(
        f"Comandos de {bot.user.name}\n"
        f"!nixis El bot saluda al usuario\n"
        f"!nixis-help muestra este texto\n"
        f"!nixis-status muestra datos sobre el estado del servidor\n"
    )



@bot.command(name="nixis")
async def hola(ctx):
    print(f"INFO: {ctx.author} solicita un saludo")
    await ctx.send(f"Hola! {ctx.author}, soy {bot.user.name}! Un bot que se encargará de la gestion en discord de Selunecraft, un placer!")

@bot.command(name="nixis-status")
async def mcstatus(ctx):
    print(f"INFO: Solicitados datos del servidor desde Discord por {ctx.author}")
    try:
        server = await JavaServer.async_lookup(f"{mc_ip}:{mc_port}")
        status = await server.async_status()
        playerlist = status.players.sample
        names = ", ".join([p.name for p in playerlist]) if playerlist else "Ninguno"
        await ctx.send(
            f"**Server status:** ***ONLINE***\n"
            f"**Jugadores conectados:** {status.players.online}/{status.players.max}\n"
            f"**Ping:** {status.latency}ms\n"
            f"**Usuarios:** {names}"
        )
    except Exception:
        await ctx.send("***El servidor esta apagado o no responde!***")



@bot.command(name="nixis-whitelist-add")
async def whitelist_add(ctx, nick: str):

    rol_id = 1559233089207541800
    has_rol = any(role.id == rol_id for role in ctx.author.roles)

    if not has_rol:
        await ctx.send(f"Lo siento {ctx.author}, pero no posees los permisos para solicitar esta funcion!")

        return
  
    print(
        f"INFO: Solicitud de whitelist para '{nick}' por {ctx.author}"
    )  # (Opcional) Aquí podrías comprobar permisos/roles de Discord antes de ejecutar

    # Enviamos el comando RCON
    response = send_rcon_command(f"whitelist add {nick}")

    if response:
        await ctx.send(
            f"**Whitelist:** Usuario `{nick}` añadido correctamente.\n"
            f"- Respuesta consola: {response.strip()}"
        )
    else:
        await ctx.send(
            "**Error:** No se pudo conectar con la consola RCON del servidor."
        )





bot.run(bot_token)