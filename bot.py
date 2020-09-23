import discord
import requests
import time
import os
import requests
from bs4 import BeautifulSoup

raid_cookie = None

def get_raid_id(msg):
    ms = round(time.time() * 1000)
    raid_url = 'http://game.granbluefantasy.jp/rest/multiraid/start.json?_=' + str(ms) + '&t=' + str(ms + 1) + 'uid=69'
    pound_index = msg.find("#")
    raid_id = msg[pound_index + 12:pound_index + 23]
    payload = {
        "special_token":'null',
        "raid_id":raid_id,
        "action":"start",
        "is_multi":'true',
        "time":ms
    }
  
    header_cookie = os.environ['RAID_COOKIE']
    if raid_cookie is not None:
        header_cookie = raid_cookie
  
  
    headers = {
        'Host': 'game.granbluefantasy.jp',
        'Connection': 'keep-alive',
        'Content-Length': '100',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': os.environ['USER_AGENT'],
        'Content-Type': 'application/json',
        'Origin': 'http://game.granbluefantasy.jp',
        'Referer': 'http://game.granbluefantasy.jp/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': header_cookie,
        'X-VERSION': '1600846035'
    }
    r = requests.post(raid_url, headers=headers, json=payload)
    cookie = r.headers['Set-Cookie']
    midship_start = cookie.find("midship=") + 8
    midship_end = cookie.find("; ")
    midship_cookie = cookie[midship_start:midship_end]
    raid_cookie = raid_cookie[raid_cookie.find("midship="):] + "midship=" + midship_cookie
    return r.json()['twitter']['battle_id']

# Some boilerplate discord bot stuff
client = discord.Client()

@client.event
async def on_ready():
    print("The bot is ready!")
    
@client.event
async def on_message(message):
    # Don't reply to your own messages
    if message.author == client.user:
        return
        
    elif message.content.find("http://game.granbluefantasy.jp/#raid_multi/") != -1:
        await message.channel.send(get_raid_id(message))
        
    
    
# Stuff for hosting it
client.run(os.environ['TOKEN'])
