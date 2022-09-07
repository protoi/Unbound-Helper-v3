from locale import normalize
import discord
import os
import numpy as np
import pandas as pd
import json
import helperfunctions
import constants
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# other than the tm list, everything is probably easier to query

#################################### GENERATING DICTIONARIES ###########################################
with open("DATA/abilities.json", encoding='utf8') as file:
    abilities_dict = helperfunctions.listToDict('name',  json.load(file))
with open("DATA/ability_description.json", encoding='utf8') as file:
    ability_desc_dict = helperfunctions.listToDict('name',  json.load(file))
with open("DATA/eggmoves.json", encoding='utf8') as file:
    eggmoves_dict = helperfunctions.listToDict('name',  json.load(file))
with open("DATA/helditem.json", encoding='utf8') as file:
    helditem_dict = helperfunctions.listToDict('itemname',  json.load(file))
with open("DATA/lvlupmoves.json", encoding='utf8') as file:
    lvlupmoves_dict = helperfunctions.listToDict('name',  json.load(file))
with open("DATA/megastone.json", encoding='utf8') as file:
    megastone_dict = helperfunctions.listToDict('name',  json.load(file))
with open("DATA/pokelocation.json", encoding='utf8') as file:
    pokelocation_dict = helperfunctions.listToDict('name',  json.load(file))
with open("DATA/scalemon.json", encoding='utf8') as file:
    scalemon_dict = helperfunctions.listToDict('name',  json.load(file))
with open("DATA/tmlocation.json", encoding='utf8') as file:
    tmlocation_dict = helperfunctions.listToDict('tmname',  json.load(file))
with open("DATA/tm_and_tutor.json", encoding='utf8') as file:
    tm_and_tutor_dict = helperfunctions.listToDict('name',  json.load(file))
with open("DATA/zlocation.json", encoding='utf8') as file:
    zlocation_dict = helperfunctions.listToDict('name',  json.load(file))
with open("DATA/PokemonStatsNormal.json", encoding='utf8') as file:
    normal_stats_dict = helperfunctions.listToDict('name',  json.load(file))
######################################################################################################


@client.event
async def on_ready():
    print(f'{client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# client.run(os.getenv('tok'))

# sets hp to 1, attack to 2, etc 
#s = constants.stat_display.format(1, 2, 3, 4, 5, 6)
s = helperfunctions.StringFormatter(constants.stat_display, 1,2,3,4,5,6)

#prints the stats formatted
print(s)

print(tmlocation_dict[helperfunctions.normalizeString('focus                       punch')]) #<- returns a dictionary



#normalizes string to galarian darmanitan
dic = abilities_dict[helperfunctions.normalizeString('GALARIAN darManiTAN')]
#sets name to the "name" field from galarian darmanitan in the query
name = dic['name']
#sets the ability dict to the "abilities" field in the galarian darmanitan entry 
ability = dic['Ability']

ability_info = helperfunctions.StringFormatter(constants.ability_display, ability[0], ability[1], ability[2])
#prints "ability for Galarian Darmanitan: 
#        Ability 1:Gorilla Tactics
#        Ability 2:None
#        Hidden Ability:Zen Mode"
print(f'ability for {name}:\n{ability_info}')