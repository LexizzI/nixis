from dotenv import load_dotenv
from mcstatus import JavaServer
from discord.ext import commands
from discord.ext import tasks
import discord
import os

# Carga y verificacion de variables de entorno

load_dotenv()

bot_token = os.getenv("DISCORD_SK")
mc_ip = os.getenv("MC_SERVER_IP")
mc_port = os.getenv("MC_SERVER_PORT")

if mc_ip and mc_port is None:
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
        
        presence_text = f"Selunecraft [{status.players.online}/{status.players.max}] - En linea!"
        
        await bot.change_presence(activity=discord.Game(name=presence_text))
        
    except Exception:
        await bot.change_presence(activity=discord.Game(name="Selunecraft [offline]"))


@bot.event
async def on_ready():
    rpc_update.start()
    print(f"Hola! Soy {bot.user.name}, todos los parametros correctos, lista para funcionar!")
    

# bloque con las funciones de los comandos

@bot.command(name="nixis-help")
async def help(ctx):
    print(f"INFO: El usuario {ctx.author} ha solicitado el comando de ayuda")
    await ctx.send(
        f"***Comandos de {bot.user.name}***\n"
        f"**!nixis** *El bot saluda al usuario*\n"
        f"**!nixis-help** *muestra este texto*\n"
        f"**!nixis-status** *muestra datos sobre el estado del servidor*\n"
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
        await ctx.send(
            f"***Server status: ONLINE***\n"
            f"**Jugadores conectados:** {status.players.online}/{status.players.max}\n"
            f"**Ping:** {status.latency}ms\n"
            f"**Usuarios:** {status.players.sample}\n"
        )
    except Exception:
        await ctx.send("***El servidor esta apagado o no responde!***")

bot.run(bot_token)