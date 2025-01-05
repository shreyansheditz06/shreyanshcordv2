import os
os.system("pip install --upgrade pip")
import json
import string
import discord, aiohttp
from discord.ext import commands, tasks
import requests
from colorama import Fore, Style
import qrcode
import asyncio
import requests
import sys
import random
from flask import Flask
from threading import Thread
import threading
import subprocess
import requests
import time
from discord import Color, Embed
import colorama
import urllib.parse
import urllib.request
import re
from pystyle import Center, Colorate, Colors
from io import BytesIO
import webbrowser
from bs4 import BeautifulSoup
import datetime
from pyfiglet import Figlet
from discord import Member
import openai
from dateutil import parser
from collections import deque
from googletrans import Translator, LANGUAGES
import image
import afk

colorama.init()

intents = discord.Intents.default()
intents.presences = True
intents.guilds = True
intents.typing = True
intents.presences = True
intents.dm_messages = True
intents.messages = True
intents.members = True
intents.guild_messages = True

category_messages = {}
active_tasks = {}
sent_channels = set()

def load_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    return config


if __name__ == "__main__":
    config_file_path = "config.json"
    config = load_config(config_file_path)

#=== Welcome ===
prefix = config.get('prefix')
token = config.get('token')
api_key = config.get('apikey')
ltc_priv_key = config.get('ltckey')
ltc_addy = config.get("LTC_ADDY")
I2C_Rate = config.get("I2C_Rate")
C2I_Rate = config.get("C2I_Rate")
LTC = config.get("LTC_ADDY")
Upi = config.get("Upi")
upi_id = config.get("Upi")
Qr = config.get("Qr")
User _Id = config.get("User _Id")
SERVER_Link = config.get("SERVER_Link")
#===================================

shreyansh = commands.Bot(description='SELFBOT CREATED BY Shreyansh',
                           command_prefix=prefix,
                           self_bot=True,
                           intents=intents)
status_task = None

shreyansh.remove_command('help')

shreyansh.whitelisted_users = {}

shreyansh.antiraid = False

red = "\033[91m"
yellow = "\033[93m"
green = "\033[92m"
blue = "\033[36m"
pretty = "\033[95m"
magenta = "\033[35m"
lightblue = "\033[94m"
cyan = "\033[96m"
gray = "\033[37m"
reset = "\033[0m"
pink = "\033[95m"
dark_green = "\033[92m"
yellow_bg = "\033[43m"
clear_line = "\033[K"

@shreyansh.event
async def on_ready():
      print(
        Center.XCenter(
            Colorate.Vertical(
                Colors.red_to_purple,
            f"""[=]-------------------------------------------------------------------------------------------[=]
[  Bot -  MADED  BY  :-  shreyansh  -  LOGINED  AS  :-  {shreyansh.user.name}  ]
[=]-------------------------------------------------------------------------------------------[=]
""",
                1,
            )
        )
    )


def load_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    return config


if __name__ == "__main__":
    config_file_path = "config.json"
    config = load_config(config_file_path)

#=== Welcome ===
prefix = config.get('prefix')
token = config.get('token')
api_key = config.get('apikey')
ltc_priv_key = config.get('ltckey')
ltc_addy = config.get("LTC_ADDY")
I2C_Rate = config.get("I2C_Rate")
C2I_Rate = config.get("C2I_Rate")
LTC = config.get("LTC_ADDY")
Upi = config.get("Upi")
upi_id = config.get("Upi")
Qr = config.get("Qr")
User _Id = config.get("User _Id")
SERVER_Link = config.get("SERVER_Link")
#===================================

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d }".format(hour, minute, second)
    return timee

time_rn = get_time_rn()

@shreyansh.event
async def on_message(message):
    if message.author.bot:
        return

    # Auto-response handling
    with open('ar.json', 'r') as file:
        auto_responses = json.load(file)

    if message.content in auto_responses:
        await message.channel.send(auto_responses[message.content])

    await shreyansh.process_commands(message)
    
    # Auto-message handling
def load_auto_messages():
    try:
        with open("am.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_auto_messages(data):
    with open("am.json", "w") as f:
        json.dump(data, f, indent=4)
        
#Discord Status Changer Class
class DiscordStatusChanger:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": token,
            "User -Agent": "DiscordBot (https://discordapp.com, v1.0)",
            "Content-Type": "application/json",
            "Accept": "*/*"
        }

    def change_status(self, status, message, emoji_name, emoji_id):
        jsonData = {
            "status": status,
            "custom_status": {
                "text": message,
                "emoji_name": emoji_name,
                "emoji_id": emoji_id,
            }
        }
        r = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=self.headers, json=jsonData)
        return r.status_code
    
class StatusRotator(commands.Cog):
    def __init__(self, shreyansh, token):
        self.bot = shreyansh
        self.token = config.get('token')
        self.discord_status_changer = DiscordStatusChanger(self.token)
        self.is_rotating = False  # New attribute to control rotation

    @commands.command()
    async def start_rotation(self, ctx):
        if not self.is_rotating:
            self.is_rotating = True
            await ctx.send("**Starting Status Rotation**")
            await self.run_rotation(ctx)
        else:
            await ctx.send("**Status Rotation Is Already Running**")

    @commands.command()
    async def stop_rotation(self, ctx):
        if self.is_rotating:
            self.is_rotating = False
            await ctx.send("Stopping Status Rotation")
        else:
            await ctx.send("Status Rotation Is Not Currently Running.")

    async def run_rotation(self, ctx):
        file_path = 'status.txt'
        while self.is_rotating:
            try:
                with open(file_path, 'r') as file:
                    messages = [line.strip() for line in file.readlines()]

                if not messages:
                    await ctx.send("No Messages Found In The File. Add Messages To Continue.")
                    await asyncio.sleep(30)
                    continue

                for message in messages:
                    message_parts = message.split(',')

                    if len(message_parts) >= 2:
                        emoji_id = None
                        emoji_name = message_parts[0].strip()

                        if emoji_name and emoji_name[0].isdigit():
                            emoji_id = emoji_name
                            emoji_name = ""

                        status_text = message_parts[1].strip()

                        status_code = self.discord_status_changer.change_status("dnd", status_text, emoji_name, emoji_id)
                        if status_code == 200:
                            print(f"Changed To: {status_text}")
                        else:
                            print("Failed To Change Status")
                        await asyncio.sleep(10)
            
            except Exception as e:
                print(f"An Error Occurred: {e}")
                await asyncio.sleep(10)  # Retry after 10 seconds
                
TOKEN = config.get('token')
shreyansh.add_cog(StatusRotator(shreyansh, TOKEN))


#task
tasks_dict = {}

@shreyansh.command()
async def help(ctx):
    message = '''# - ** LUX SELF BOT 1** -

- **SHOW ALLCMDS - .help**
- **SRV CLONE - .csrv <copy id> <target id>**
- **CREATE CHNL/ROLE - .role/.chnl <chnl/role name>**
- **VOUCH - .vouch <product for price>**
- **EXCH VOUCH - .exch <which to which>**
- **UPI ID - .upi**
- **QR CODE :- .qr**
- **CUSTOM QR - .cqr <amt> <note>**
- **SEND LTC - .send <addy> <amount>**
- **CHECK BALANCE - .bal <addy>**
- **CHECK MYBAL - .mybal**
- **LTC ADDY - . ```python
addy**
- **CRYPTO PRICE IN USD - .ltc/sol/btc/usdt**
- **CALCULATE - .math <equation>**
- **INR TO CRYPTO - .i2c <inr amount>**
- **CRYPTO TO INR - .c2i <crypto amount>**
- **LTC TO USD - .l2u <ltc amount>**
- **USD TO LTC - .u2l <usd amount>**
- **CHECK PROMO - .checkpromo <promo>**
- **CHECK TOKEN - .checktoken <token>**
- **FOR MORE COMMENDS- .MORE**


'''
    await ctx.send(message)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} HELP SENT SUCCESFULLY✅ ")
    await ctx.message.delete()

@shreyansh.command()
async def more(ctx):
    message = '''# - ** LUX SELF BOT 2** -

- **GET AVATAR - .avatar <@user>**
- **GET ICON OF SERVER - .icon**
- **GET IMAGE - .get_image <query>**
- **SNIPE DELETED MSG - .snipe**
- **TRANSLATE MSG - .translate <msg>**
- **DM ALL IN SERVER - .dmall <msg>**
- **MASS DM FRIENDS - .massdmfrnds <msg>**
- **YT SEARCH - .yt <title-search>**
- **AUTORESPOND - .ar <trigger>, <response>**
- **REMOVE RESPOND - .removear <triger>**
- **AUTORESPOND List - .ar_list**
- **AUTOMSG - .am <time> <chnl_id> <msg>**
- **STOP AUTOMSG - .am_stop <chnl_id>**
- **AUTOMSG LIST - .am_list**
- **FOR MORE COMMENDS- .MOREE**


'''
    await ctx.send(message)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} HELP SENT SUCCESFULLY✅ ")
    await ctx.message.delete()

@shreyansh.command()
async def moree(ctx):
    message = '''# - ** LUX SELF BOT 3** -

- **OWO GRIND START - .owostart**
- **OWO GRIND STOP - .owostop**
- **ABUSE - .abuse <user>**
- **SAVE TRANSCRIPT - .savetrs**
- **MASS REACT - .massreact <emote>**
- **HIDE - .hide**
- **UNHIDE - .unhide**
- **RESTART BOT - .restart**
- **NUKE SERVER - .nukesrv**
- **GEN JOKE - .joke**
- **GEN MEME - .meme**
- **SERVER INFO - .srvinfo**
- **SELFBOT INFO - .selfbot**
- **USER INFO - .user_info**
- **STATUS ROTATOR - .rotate <emoji id , msg> / <emoji id , msg> / <repeat again>**
- **STOP ROTATOR - .stop_rotate**
- **CREATE STATUS - .stream/play/watch/listen <title>**
- **REMOVE STATUS - .stopactivity**
- **AFK - .afk <reason>**
- **REMOVE AFK - .unafk**
- **SPAM MSG - .spam <amount> <msg>**
- **CLEAR MSG - .clear <amount>**
- **DIRECT MSG - .dm <@user> <msg>**
'''
    await ctx.send(message)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} HELP SENT SUCCESFULLY✅ ")
    await ctx.message.delete()

@shreyansh.command()
async def upi(ctx):
    message = (f"- **UPI** -")
    message2 = (f"{Upi}")
    message3 = (f"**MUST SEND SCREENSHOT AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    await ctx.send(message3)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} UPI SENT SUCCESFULLY✅ ")
    await ctx.message.delete()

@shreyansh.command()
async def qr(ctx):
    message = (f"{Qr}")
    message2 = (f"**MUST SEND SCREENSHOT AFTER PAYMENT**")
    await ctx.send(message)
    await ctx send(message2)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} QR SENT SUCCESFULLY✅ ")
    await ctx.message.delete()

@shreyansh.command()
async def addy(ctx):
    message = (f"- **LTC ADDY** -")
    message2 = (f"{LTC}")
    message3 = (f"**MUST SEND SCREENSHOT AND BLOCKCHAIN AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    await ctx.send(message3)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} ADDY SENT SUCCESFULLY✅ ")
    await ctx.message.delete()

# MATHS
api_endpoint = 'https://api.mathjs.org/v4/'
@shreyansh.command()
async def math(ctx, *, equation):
    response = requests.get(api_endpoint, params={'expr': equation})

    if response.status_code == 200:
        result = response.text
        await ctx.send(f'- **EQUATION**: `{equation}`\n\n- **Result**: `{result}`')
        await ctx.message.delete()
    else:
        await ctx.reply('- **Failed**')

@shreyansh.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def i2c(ctx, amount: str):
    amount = float(amount.replace('₹', ''))
    inr_amount = amount / I2C_Rate
    await ctx.send(f"- **EQUATION**: `{amount}/{I2C_Rate}`\n\n- **Result** : `${inr_amount:.2f}`")
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} I2C DONE✅ ")

@shreyansh.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def c2i(ctx, amount: str):
    amount = float(amount.replace('$', ''))
    usd_amount = amount * C2I_Rate
    await ctx.send(f"- **EQUATION**: `{amount}*{C2I_Rate}`\n\n- **Result** : `₹{usd_amount:.2f}`")
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} C2I DONE✅ ")

spamming_flag = True
# SPAM 
@shreyansh.command()
async def spam(ctx, times: int, *, message):
    for _ in range(times):
        await ctx.send(message)
        await asyncio.sleep(0.1)      
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty} {Fore.GREEN} SPAMMING SUCCESFULLY✅ ")

@shreyansh.command(aliases=[])
async def mybal(ctx):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{LTC}/balance')

    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.reply("- `Failed`")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.reply("- `Failed`")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price
    
    message = f"- **ADDY**: `{LTC}` -\n"
    message += f"- **CURRENT LTC BALANCE** : `{usd_balance:.2f}$ USD` -\n"
    message += f"- **TOTAL LTC RECEIVED** : `{usd_total_balance:.2f}$ USD` -\n"
    message += f"- **UNCONFIRMED LTC** : `{usd_unconfirmed_balance:.2f}$ USD` -\n\n"

    await ctx.send(message)
    await ctx.message.delete()

@shreyansh.command(aliases=['ltcbal'])
 ```python
async def bal(ctx, ltcaddress):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')

    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.reply("- `Failed`")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.reply("- `Failed`")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price
    
    message = f"- **ADDY**: `{ltcaddress}` -\n"
    message += f"- **CURRENT LTC BALANCE** : `{usd_balance:.2f}$ USD` -\n"
    message += f"- **TOTAL LTC RECEIVED** : `{usd_total_balance:.2f}$ USD` -\n"
    message += f"- **UNCONFIRMED LTC** : `{usd_unconfirmed_balance:.2f}$ USD` -\n\n"

    await ctx.send(message)
    await ctx.message.delete()

@shreyansh.command(aliases=["streaming"])
async def stream(ctx, *, message):
    stream = discord.Streaming(
        name=message,
        url="https://twitch.tv/fahimxshahrear",
    )
    await shreyansh.change_presence(activity=stream)
    await ctx.send(f"- **Stream Created** : `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} STREAM SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@shreyansh.command(aliases=["playing"])
async def play(ctx, *, message):
    game = discord.Game(name=message)
    await shreyansh.change_presence(activity=game)
    await ctx.send(f"- **Status For PLAYZ Created** : `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} PLAYING SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@shreyansh.command(aliases=["watch"])
async def watching(ctx, *, message):
    await shreyansh.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=message,
    ))
    await ctx.send(f"- **Watching Created**: `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} WATCH SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@shreyansh.command(aliases=["listen"])
async def listening(ctx, *, message):
    await shreyansh.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=message,
    ))
    await ctx.reply(f"- **Listening Created**: `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} STATUS SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@shreyansh.command(aliases=[
    "stopstreaming", "stopstatus", "stoplistening", "stopplaying",
    "stopwatching"
])
async def stopactivity(ctx):
    await ctx.message.delete()
    await shreyansh.change_presence(activity=None, status=discord.Status.dnd)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} STREAM SUCCESFULLY STOPED⚠️ ")

@shreyansh.command()
async def exch(ctx, *, text):
    await ctx.message.delete()
    main = text
    await ctx.send(f'+rep {User _Id} LEGIT | EXCHANGED {main} • TYSM')
    await ctx.send(f'{SERVER_Link}')
    await ctx.send(f'**PLEASE VOUCH ME HERE**')
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} EXCH VOUCH✅ ")

@shreyansh.command()
 async def vouch(ctx, *, text):
    await ctx.message.delete()
    main = text
    await ctx.send(f'+rep {User  _Id} LEGIT SELLER | GOT {main} • TYSM')
    await ctx.send(f'{SERVER_Link}')
    await ctx.send(f'**PLEASE VOUCH ME HERE**')
    await ctx.send(f'**NO VOUCH NO WARRANTY OF PRODUCT**')
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} VOUCH SENT✅ ")

@shreyansh.command(aliases=['cltc'])
async def ltcprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/litecoin'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"- **The Price Of Ltc Is :** `{price:.2f}`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} LTC PRICE SENT✅ ")
    else:
        await ctx.send("**Failed To Fetch**")

@shreyansh.command(aliases=['csol'])
async def solprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/solana'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"- **The Price Of Sol Is :** `{price:.2f}`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} SOL PRICE SENT✅ ")
    else:
        await ctx.send("**Failed To Fetch**")

@shreyansh.command(aliases=['cusdt'])
async def usdtprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/tether'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"- **The Price Of Usdt Is :** `{price:.2f}`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} USDT PRICE SENT✅ ")
    else:
        await ctx.send("**Failed To Fetch**")

@shreyansh.command(aliases=['cbtc'])
async def btcprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"- **The Price Of Btc Is :** `{price:.2f}`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} BTC PRICE SENT✅ ")
    else:
        await ctx.send("**Failed To Fetch**")

@shreyansh.command()
async def ar(ctx, *, trigger_and_response: str):
    trigger, response = map(str.strip, trigger_and_response.split(','))

    with open('ar.json', 'r') as file:
        data = json.load(file)

    data[trigger] = response

    with open('ar.json', 'w') as file:
        json.dump(data, file, indent=4)

    await ctx.send(f'- **Auto Response Has Added.. !** **{trigger}** - **{response}**')
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} AUTO RESPOND ADDED✅ ")

@shreyansh.command()
async def removear(ctx, trigger: str):
    with open('ar.json', 'r') as file:
        data = json.load(file)

    if trigger in data:
        del data[trigger]

        with open('ar.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send(f'- **Auto Response Has Removed** **{trigger}**')
        await ctx.message.delete()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} AUTO RESPOND REMOVE✅ ")
    else:
        await ctx.send(f'- **Auto Response Not Found** **{trigger}**')

@shreyansh.command()
async def ar_list(ctx):
    with open("ar.json", "r") as f:
        data = f.read()
    await ctx.send(data)
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty} {Fore.GREEN} ar_list Command Used✅ ")

@shreyansh.command()
async def am_list(ctx):
    with open("am.json", "r") as f:
        data = f.read()
    await ctx.send(data)
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty} {Fore.GREEN} am_list Command Used✅ ")

@shreyansh.command()
async def csrv(ctx, source_guild_id: int, target_guild_id: int):
    source_guild = shreyansh.get_guild(source_guild_id)
    target_guild = shreyansh.get_guild(target_guild_id)

    if not source_guild or not target_guild:
        await ctx.send("- **Guild Not Found**")
        return

    for channel in target_guild.channels:
        try:
            await channel.delete()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN DELETED ON THE TARGET GUILD✅ ")
            await asyncio.sleep(0)
        except Exception as e:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR DELETING CHANNEL {channel.name}: {e}")

    for role in target_guild.roles:
        if role.name not in ["here", "@everyone"]:
            try:
                await role.delete()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} ROLE {role.name} HAS BEEN DELETED ON THE TARGET GUILD✅ ")
                await asyncio.sleep(0)
            except Exception as e:
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR DELETING ROLE {role.name}: {e}")

    roles = sorted(source_guild.roles, key=lambda role: role.position)

    for role in roles:
        try:
            new_role = await target_guild.create_role(name=role.name, permissions=role.permissions, color=role.color, hoist=role.hoist, mentionable=role.mentionable)
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} {role.name} HAS BEEN CREATED ON THE TARGET GUILD✅ ")
            await asyncio.sleep(0)

            for perm, value in role.permissions:
                await new_role.edit_permissions(target_guild.default_role, **{perm: value})
        except Exception as e:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR CREATING ROLE {role.name}: {e}")

    text_channels = sorted(source_guild.text_channels, key=lambda channel: channel.position)
    voice_channels = sorted(source_guild.voice_channels, key=lambda channel: channel.position)
    category_mapping = {}

    for channel in text_channels + voice_channels:
        try:
            if channel.category:
                if channel.category.id not in category_mapping:
                    category_perms = channel.category.overwrites
                    new_category = await target_guild.create_category_channel(name=channel.category.name, overwrites=category_perms)
                    category_mapping[channel.category.id] = new_category

                if isinstance(channel, discord.TextChannel):
                    new_channel = await new_category.create_text_channel(name=channel.name)
                elif isinstance(channel, discord.VoiceChannel):
                    existing_channels = [c for c in new_category.channels if isinstance(c, discord.VoiceChannel) and c.name == channel.name]
                    if existing_channels:
                        new_channel = existing_channels[0]
                    else:
                        new_channel = await new_category.create_voice_channel(name=channel.name)

                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN CREATED ON THE TARGET GUILD✅ ")

                for overwrite in channel.overwrites:
                    if isinstance(overwrite.target, discord.Role):
                        target_role = target_guild.get_role(overwrite.target.id)
                        if target_role:
 await new_channel.set_permissions(target_role, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))
                    elif isinstance(overwrite.target, discord.Member):
                        target_member = target_guild.get_member(overwrite.target.id)
                        if target_member:
                            await new_channel.set_permissions(target_member, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))

                await asyncio.sleep(0)
            else:
                if isinstance(channel, discord.TextChannel):
                    new_channel = await target_guild.create_text_channel(name=channel.name)
                elif isinstance(channel, discord.VoiceChannel):
                    new_channel = await target_guild.create_voice_channel(name=channel.name)

                for overwrite in channel.overwrites:
                    if isinstance(overwrite.target, discord.Role):
                        target_role = target_guild.get_role(overwrite.target.id)
                        if target_role:
                            await new_channel.set_permissions(target_role, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))
                    elif isinstance(overwrite.target, discord.Member):
                        target_member = target_guild.get_member(overwrite.target.id)
                        if target_member:
                            await new_channel.set_permissions(target_member, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))

                await asyncio.sleep(0)

                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN CREATED ON THE TARGET GUILD✅ ")

        except Exception as e:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR CREATING CHANNEL {channel.name}: {e}")

@shreyansh.command(aliases=["pay", "sendltc"])
async def send(ctx, addy, value):
    try:
        value = float(value.strip('$'))
        message = await ctx.send(f"- **Sending {value}$ To :-** {addy}")
        url = "https://api.tatum.io/v3/litecoin/transaction"
        
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=usd&vs_currencies=ltc")
        r.raise_for_status()
        usd_price = r.json()['usd']['ltc']
        topay = usd_price * value
        
        payload = {
            "fromAddress": [
                {
                    "address": ltc_addy,
                    "privateKey": ltc_priv_key
                }
            ],
            "to": [
                {
                    "address": addy,
                    "value": round(topay, 8)
                }
            ],
            "fee": "0.00005",
            "changeAddress": ltc_addy
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": api_key
        }

        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        await message.edit(content=f"- **Successfully Sent {value}$ To {addy}**\nhttps://blockchair.com/litecoin/transaction/{response_data['txId']}")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} LTC SEND SUCCESS✅ ")
    except Exception as e:
        await ctx.send(content=f"- **Failed to send LTC Because** :- {str(e)}")

@shreyansh.command(aliases=['purge', 'clear'])
async def clear(ctx, times: int):
    channel = ctx.channel

    def is_bot_message(message):
        return message.author.id == ctx.bot.user.id

    messages = await channel.history(limit=times + 1).flatten()

    bot_messages = filter(is_bot_message, messages)

    for message in bot_messages:
        await asyncio.sleep(0.55)  
        await message.delete()

    await ctx.send(f"- **Deleted {times} Messages**")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} PURGED SUCCESFULLY✅ ")

@shreyansh.command()
async def user_info(ctx, user: discord.User):
    info = f'''## User Info
    - **Name** : `{user.name}`
    - **Display Name** ```python
: `{user.display_name}`
    - **User  Id** : `{user.id}`
    - **User  Avatar** : {user.avatar_url}
    '''
    await ctx.send(info)
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} USER INFO SUCCESFULLY✅ ")

@shreyansh.command()
async def am(ctx, time_in_sec: int, channel_id: int, *, content: str):
    channel = shreyansh.get_channel(channel_id)
    await ctx.message.delete()
    
    if channel is None:
        await ctx.send("- `Channel not found.`")
        return

    if time_in_sec <= 0:
        await ctx.send("- `Time must be greater than 0.`")
        return

    auto_messages = load_auto_messages()

    if str(channel_id) in auto_messages:
        await ctx.send(f"- **Auto Message already exists for channel {channel_id}.**")
        return

    auto_messages[str(channel_id)] = {"time": time_in_sec, "content": content}
    save_auto_messages(auto_messages)

    @tasks.loop(seconds=time_in_sec)
    async def auto_message_task():
        await channel.send(content)

    auto_message_task.start()
    tasks_dict[channel_id] = auto_message_task
    
    await ctx.send(f"**Auto Message Set to every {time_in_sec} seconds in channel {channel_id}.**")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty} {Fore.GREEN} Automessage Set Succesfully✅ ")

@shreyansh.command()
async def am_stop(ctx, channel_id: int):
    await ctx.message.delete()
    if channel_id in tasks_dict:
        tasks_dict[channel_id].stop()
        del tasks_dict[channel_id]

        auto_messages = load_auto_messages()
        auto_messages.pop(str(channel_id), None)
        save_auto_messages(auto_messages)
        
        await ctx.send(f"- **Auto Message Stopped for channel {channel_id}.**")
        print("Automessage Stopped Succesfully")
    else:
        await ctx.send("- `No auto message task found for this channel.`")

def generate_upi_qr(amount, note):
    upi_url = f"upi://pay?pa={upi_id}&am={amount}&cu=INR&tn={note}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)

    return buffer
        
@shreyansh.command(name='upiqr')
async def upiqr(ctx, amount: str, *, note: str):
    await ctx.message.delete()
    try:
        buffer = generate_upi_qr(amount, note)
        await ctx.send(file=discord.File(fp=buffer, filename='upi_qr.png'))
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
            
@shreyansh.command(name='joke')
async def joke(ctx):
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    joke = response.json()
    await ctx.send(f"- {joke['setup']} - {joke['punchline']}")
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} JOKE✅ ")

@shreyansh.command(name='meme')
async def meme(ctx):
    response = requests.get('https://meme-api.com/gimme')
    meme = response.json()
    await ctx.send(meme['url'])
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} MEME✅ ")

@shreyansh.command()
async def dm(ctx, user: discord.User, *, message):
    await ctx.message.delete()
    try:
        await user.send(f"{message}")
        await ctx.send(f"[+] Successfully DM {user.name}")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} DM SENT✅ ")
    except discord.Forbidden:
        await ctx.send(f"[-] Cannot DM {user.name}, permission denied.")
    except discord.HTTP Exception as e:
        await ctx.send(f"[-] Failed to DM {user.name} due to an HTTP error: {e}")
    except Exception as e:
        await ctx.send(f"[-] An unexpected error occurred when DMing {user.name}: {e}")

@shreyansh.command()
async def l2u(ctx, ltc_amt: float):
    await ctx.message.delete()
    try:
        coingecko_resp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
        coingecko_resp.raise_for_status()
        ltc_to_usd_rate = coingecko_resp.json()['litecoin']['usd']
        output = ltc_amt * ltc_to_usd_rate
        await ctx.send(f"- **EQUATION**: `{ltc_amt}*{ltc_to_usd_rate}`\n\n- `{ltc_amt} LTC = {output} USD`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} L2U✅ ")
    except requests.RequestException as e:
        await ctx.send(f"- `Error fetching Litecoin price: {e}`")

@shreyansh.command()
async def u2l(ctx, usd_amt: float):
    await ctx.message.delete()
    try:
        coingecko_resp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
        coingecko_resp.raise_for_status()
        ltc_to_usd_rate = coingecko_resp.json()['litecoin']['usd']
        output = usd_amt / ltc_to_usd_rate
        await ctx.send(f"- **EQUATION**: `{usd_amt}/{ltc_to_usd_rate}`\n\n- `{usd_amt} USD = {output} LTC`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} U2L✅ ")
    except requests.RequestException as e:
        await ctx.send(f"- `Error fetching Litecoin price: {e}`")

@shreyansh.command()
async def support(ctx, *, message):
    await ctx.message.delete()
    msg = {
        "content": f"## Received New Support Message\n- **Message Sent By {ctx.author.name} ID {ctx.author.id}**\n**Message Content** = `{message}`"
    }
    try:
        r = requests.post("https://discord.com/api/webhooks/1293649266438574090/V1qmzOe3vvEKIeSzlfAiIxQM0dn0SiUvoFWfQHqOA2HFBMYLsL0gIn5lq1ea1JJl8vaz", json=msg)
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty} {Fore.GREEN} Support Message Sent Succesfully ✅")
        await ctx.send("**Support Message Sent Succesfully**")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} SUPPORT✅ ")
    except:
        await ctx.send("**Failed. Can't Send Message To Support Team Webhook Please Join For Manual Support [Server Link](-)**")

@shreyansh.command()
async def selfbot(ctx):
    await ctx.send('''**SELFBOT DETAILS**
- **NAME** > Shreyansh
- **VERSION** > 1
- **DEVELOPER** > `Shreyansh`
- **SUPPORT SERVER** > [SUPPORT](-)''')
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} SELFBOT INFO✅ ")

@shreyansh.command()
async def checkpromo(ctx, *, promo_links):
    await ctx.message.delete()
    links = promo_links.split('\n')

    async with aiohttp.ClientSession() as session:
        for link in links:
            promo_code = extract_promo_code(link)
            if promo_code:
                result = await check_promo(session, promo_code, ctx)
                await ctx.send(result)
            else:
                await ctx.send(f'- **INVALID LINK** : `{link}`')

async def check_promo(session, promo_code, ctx):
    url = f'https://ptb.discord.com/api/v10/entitlements/gift-codes/{promo_code}'

    async with ```python
session.get(url) as response:
        if response.status in [200, 204, 201]:
            data = await response.json()
            if data["uses"] == data["max_uses"]:
                return f'- **Code:** {promo_code}\n- **Status:** ALREADY CLAIMED'
            else:
                try:
                    now = datetime.datetime.utcnow()
                    exp_at = data["expires_at"].split(".")[0]
                    parsed = parser.parse(exp_at)
                    days = abs((now - parsed).days)
                    title = data["promotion"]["inbound_header_text"]
                except Exception as e:
                    print(e)
                    exp_at = "- `FAILED TO FETCH`"
                    days = ""
                    title = "- `FAILED TO FETCH`"
                return (f'- **Code:** {promo_code}\n'
                        f'- **Expiry Date:** {days} days\n'
                        f'- **Expires At:** {exp_at}\n'
                        f'- **Title:** {title}')
                
        elif response.status == 429:
            return '- **RARE LIMITED**'
        else:
            return f'- **INVALID CODE** : `{promo_code}`'

def extract_promo_code(promo_link):
    promo_code = promo_link.split('/')[-1]
    return promo_code

deleted_messages = {}

@shreyansh.event
async def on_message_delete(message):
    if message.guild:
        if message.channel.id not in deleted_messages:
            deleted_messages[message.channel.id] = deque(maxlen=5)  # Store up to 5 messages

        deleted_messages[message.channel.id].append({
            'content': message.content,
            'author': message.author.name,
            'timestamp': message.created_at
        })

@shreyansh.command()
async def snipe(ctx):
    await ctx.message.delete()
    channel_id = ctx.channel.id
    if channel_id in deleted_messages and deleted_messages[channel_id]:
        messages = deleted_messages[channel_id]
        for msg in messages:
            timestamp = msg['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            await ctx.send(f'''### Snipped Deleted Message
{timestamp} | Message Content : `{msg["content"]}`

Message sent By `{msg['author']}`''')
    else:
        await ctx.send("- No messages to snipe in this channel.")

@shreyansh.command()
async def checktoken(ctx, tooken):
    await ctx.message.delete()
    headers = {
        'Authorization': tooken
    }
    r = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if r.status_code == 200:
        user_info = r.json()
        await ctx.send(f'''### Token Checked Succesfully
              - **Valid Token**
              - **Username : `{user_info["username"]}`**
              - **User  Id : `{user_info["id"]}`**
              - **Email : `{user_info["email"]}`**
              - **Verified? `{user_info["verified"]}`''')
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} TOKEN CHECKED✅ ")
    else:
        await ctx.send("- Invalid Token or Locked or flagged")

translator = Translator()

@shreyansh.command()
async def translate(ctx, *, text: str):
    await ctx.message.delete()
    try:
        detection = translator.detect(text)
        source_language = detection.lang
        source_language_name = LANGUAGES.get(source_language, 'Unknown language')

        translation = translator.translate(text, dest='en')
        translated_text = translation.text

        response_message = (
            f"- **Original Text:** {text}\n"
            f"- **Detected Language:** {source_language_name} ({source_language})\n"
            f"- **Translated Text:** {translated_text}"
        )

        await ctx.send(response_message)
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} MSG TRANSLATED✅ ")

    except Exception as e:
        await ctx.send("- **Error**: Could not translate text. Please try again later.")

@shreyansh.command()
async def avatar(ctx, user: discord.User):
    await ctx.message.delete()
    try:
        await ctx.send(user.avatar_url)
    except:
        await ctx.send("- User Don't Have Avatar")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} AVATAR✅ ")

@shreyansh.command()
async def banner(ctx, user: discord.User):
    await ctx.message.delete()
    banner_url = user.banner_url
    if banner_url:
        await ctx.send(banner_url)
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} BANNER✅ ")
    else:
        await ctx.send("- This user does not have a banner.")

@shreyansh.command()
async def icon(ctx):
    await ctx.message.delete()
    server_icon_url = ctx.guild.icon_url if ctx.guild.icon else "- No server icon"
    await ctx.send(server_icon_url)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} ICON✅ ")

@shreyansh.command()
async def get_image(ctx, query):
    await ctx.message.delete()
    params = {
        "query": query,
        'per_page': 1,
        'orientation': 'landscape'
    }
    headers = {
        'Authorization': 'Client-ID F1kSmh4MALfMKjHRxk38dZmPEV0OxsHdzuruBS_Y7to'
    }
    try:
        r = requests.get("https://api.unsplash.com/search/photos", headers=headers, params=params)
        r.raise_for_status()
        data = r.json()
        if data['results']:
            image_url = data['results'][0]['urls']['regular']
            await ctx.send(f"Here is your image for `{query}`:\n{image_url}")
            print("Successfully Generated Image")
        else:
            await ctx.send('No images found.')
    except requests.RequestException as e:
        print(f"Error fetching image: {e}")
        await ctx.send(f"`Error fetching image: {e}`")

@shreyansh.command()
async def sc(ctx, category_id: int, *, message: str):
    await ctx.message.delete()
    if ctx.guild is None:
        await ctx.send("This command can only be used in a server.")
        return

    category = discord.utils.get(ctx.guild.categories, id=category_id)
    if category is None:
        await ctx.send("Category not found.")
        return

    if category_id in active_tasks:
        await ctx.send("A message task is already running for this category. Please stop it first using `.stopmsg`.")
        return

    category_messages[category_id] = message
    active_tasks[category_id] = True

    await ctx.send(f"**Sending Msg In Ticket Create Category Id: {category.name}.**")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} TICKET MSG CATEGORY SET✅ ")

@shreyansh.event
async def on_guild_channel_create(channel):
    if isinstance(channel, discord.TextChannel):
        category_id = channel.category_id
        if category_id in active_tasks and active_tasks[category_id]:
            await asyncio.sleep(1)  # Optional delay before sending the message
            await channel.send(category_messages[category_id])

@shreyansh.command()
async def stopsc(ctx, category_id: int):
    await ctx.message.delete()
    if category_id not in active_tasks:
        await ctx.send("No message task is running for this category")
        return

    active_tasks[category_id] = False
    await ctx.send(f"**Stopped Sending Msg In Ticket Create Category Id: {category_id}.**")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} TICKET MSG CATEGORY REMOVED✅ ")

shreyansh.load_extension("afk")    

shreyansh.run(token, bot=False)