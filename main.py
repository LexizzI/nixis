import os
import re
import asyncio
from dotenv import load_dotenv
from mcstatus import JavaServer
from discord.ext import commands, tasks
from mcrcon import MCRcon
import discord

# Load and verification of environment variables
load_dotenv()

bot_token = os.getenv("DISCORD_SK")
mc_ip = os.getenv("MC_SERVER_IP")
mc_port = os.getenv("MC_SERVER_PORT")
servername = os.getenv("MC_SERVER_NAME")
rcon = os.getenv("RCON_PORT")
rcon_pswd = os.getenv("RCON_PSWD")

if not mc_ip or not mc_port:
    print("ERROR!: Minecraft server IP and port not defined in .env")
else:
    print(f"INFO: Server IP defined successfully!")

if bot_token is None:
    print("ERROR!: No Discord token found in .env")
    raise SystemExit


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)

# RPC Loop
@tasks.loop(seconds=5)
async def rpc_update():
    try:
        server = await JavaServer.async_lookup(f"{mc_ip}:{mc_port}")
        status = await server.async_status()
        
        presence_text = f"{servername} [{status.players.online}/{status.players.max}] - Online!"
        
        await bot.change_presence(activity=discord.Game(name=presence_text))
        
    except Exception:
        await bot.change_presence(activity=discord.Game(name="Server [offline]"))


@bot.event
async def on_ready():
    rpc_update.start()
    print(f"Hello! I am {bot.user.name}, all parameters correct, ready to work!")

    

# Block with command functions

@bot.command(name="nixis-help")
async def help(ctx):
    print(f"INFO: User {ctx.author} requested the help command")
    await ctx.send(
        f"{bot.user.name} commands\n"
        f"!nixis - The bot greets the user\n"
        f"!nixis-help - Displays this text\n"
        f"!nixis-status - Shows server status data\n"
    )



@bot.command(name="nixis")
async def hola(ctx):
    print(f"INFO: {ctx.author} requested a greeting")
    await ctx.send(f"Hello! {ctx.author}, I am {bot.user.name}! A bot that will handle Discord management for the server, nice to meet you!")

@bot.command(name="nixis-status")
async def mcstatus(ctx):
    print(f"INFO: Server data requested from Discord by {ctx.author}")
    try:
        server = await JavaServer.async_lookup(f"{mc_ip}:{mc_port}")
        status = await server.async_status()
        playerlist = status.players.sample
        names = ", ".join([p.name for p in playerlist]) if playerlist else "None"
        await ctx.send(
            f"**Server status:** ***ONLINE***\n"
            f"**Connected players:** {status.players.online}/{status.players.max}\n"
            f"**Ping:** {status.latency}ms\n"
            f"**Players:** {names}"
        )
    except Exception:
        await ctx.send("***The server is offline or not responding!***")

# Block for RCON whitelist management:

    # Managing the whitelist via RCON like this might not be ideal, but theoretically it works.
    # I do not recommend using RCON for this due to protocol insecurity, use responsibly and at your own risk!


def send_rcon_sync(command: str) -> str:
  """Pure synchronous function to execute MCRcon without blocking the main thread"""
  try:
    if not mc_ip or not rcon or not rcon_pswd:
      return "ERROR: Missing RCON variables in .env"

    with MCRcon(mc_ip, rcon_pswd, int(rcon)) as mcr:
      return mcr.command(command)

  except Exception as exc:
        print(f"Error: Could not execute RCON command: {exc}")
        return f"Error: {exc}"


@bot.command(name="nixis-whitelist-add")
async def whitelist_add(ctx, nick: str):
  rol_id = PLACE_YOUR_ROLE_ID_HERE
  has_rol = any(role.id == rol_id for role in ctx.author.roles)

  if not has_rol:
    await ctx.send(
        f"Sorry {ctx.author}, you do not have permissions to use this feature!"
    )
    return


  if not re.match("^[a-zA-Z0-9_]{3,16}$", nick):
    await ctx.send(
        "**Error:** The entered username is not valid (3-16 characters,"
        " alphanumeric and underscore)."
    )
    return

  print(f"INFO: Whitelist request for '{nick}' by {ctx.author}")

  response = await asyncio.to_thread(send_rcon_sync, f"whitelist add {nick}")

  if response and not response.startswith("ERROR"):
    await ctx.send(
        f"**Whitelist:** User `{nick}` added successfully.\n"
        f"- Console response: {response.strip()}"
    )
  else:
    await ctx.send(
        "**Network Error:** Could not connect to the server RCON console"
        " (Timeout / Incorrect port)."
    )



bot.run(bot_token)