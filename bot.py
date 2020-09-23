import discord
import requests
import time
import os
import requests
import random
from bs4 import BeautifulSoup

raid_cookie = "69"
gacha_cookie = "420"
data = None

def update_gacha(id):
    global data, gacha_cookie
    ms = round(time.time() * 1000)
    gacha_url = 'http://game.granbluefantasy.jp/gacha/provision_ratio/' + str(id) + '/1?_=' + str(ms) + '&t=' + str(ms + 1) + '&uid=69'
    header_cookie = os.environ['GACHA_COOKIE']
    if gacha_cookie != "420":
        header_cookie = gacha_cookie
    else:
        gacha_cookie = header_cookie
    
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
    
    r = requests.get(gacha_url, headers=headers)
    cookie = r.headers['Set-Cookie']
    midship_start = cookie.find("midship=") + 8
    midship_end = cookie.find("; ")
    midship_cookie = cookie[midship_start:midship_end]
    print(gacha_cookie)
    gacha_cookie = gacha_cookie[:gacha_cookie.find("midship=")]
    print(gacha_cookie)
    gacha_cookie += "midship=" + midship_cookie
    print(gacha_cookie)
    data = r.json()
    print(data)

def get_raid_id(msg):
    global raid_cookie
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
    if raid_cookie != "69":
        header_cookie = raid_cookie
    else:
        raid_cookie = header_cookie
  
  
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
    print(raid_cookie)
    raid_cookie = raid_cookie[:raid_cookie.find("midship=")]
    print(raid_cookie)
    raid_cookie += "midship=" + midship_cookie
    print(raid_cookie)
    return r.json()['twitter']['battle_id']

def roll():
    rarities = ["SSR", "SSR", "SR", "SR", "SR", "R", "R", "R"]
    rng = random.random()
    appear_index = 0
    item_index = 0
    item = None
    while rng > 0:
        if item_index >= len(data['appear'][appear_index]['item']):
            appear_index += 1
            item_index = 0
        item = data['appear'][appear_index]['item'][item_index]
        rng -= float(item['drop_rate'])/100.0
        item_index += 1
    print(item)
    end = "!'"
    if item['character_name'] is not None:
        end = "! It even came with a free " + item['character_name'] + "!"
    return "So lucky! You got a " + rarities[appear_index] + " " + item['name'] + end

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
        await message.channel.send(get_raid_id(message.content))
        
    elif message.content == "roll":
        await message.channel.send(roll())
        
    
update_gacha(202550)    
# Stuff for hosting it
client.run(os.environ['TOKEN'])

