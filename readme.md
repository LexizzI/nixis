# NIXIS | Minecraft Discord Bot (Practice Project)

A simple, straightforward Discord bot written in Python to practice asynchronous programming, API integration, and bot development by managing a few basic Minecraft server functions. 

> ⚠️ **Disclaimer:** This is just a personal practice project to learn Python and Discord bot development. It is not intended to be a production-ready or fully secure tool (especially regarding the use of RCON). Use it for learning and experimentation!

---

## Features

* **Rich Presence (RPC) Loop:** Continuously updates the bot's Discord activity status with the server's online player count (or shows as offline if it's down).
* **Server Status Check (`!nixis-status`):** Quick command to check if the Minecraft server is online, view the current player count, latency (ping), and a list of online players.
* **Whitelist Management (`!nixis-whitelist-add`):** Allows users with a specific Discord role to add a Minecraft username directly to the server's whitelist using RCON.
* **Basic Greetings & Help:** Simple commands (`!nixis`, `!nixis-help`) to interact with the bot.

---

## Prerequisites & Requirements

Before running the bot, make sure you have:
* Python installed.
* A registered Discord Bot application (with Message Content Intent enabled).
* A Minecraft server with RCON enabled (optional, but needed for whitelist commands).

### Dependencies
Install the required Python packages using pip:
```bash
pip install discord.py mcstatus python-dotenv mcrcon
```

---

## Configuration (`.env`)

Create a `.env` file in the root directory of your project and fill in your credentials and server details:

```env
DISCORD_SK=
MC_SERVER_IP=
MC_SERVER_PORT=
MC_SERVER_NAME=
RCON_PORT=
RCON_PSWD=  
```

---

## Running the Bot

Once your `.env` file is configured and dependencies are installed, run the script:

```bash
python bot.py
