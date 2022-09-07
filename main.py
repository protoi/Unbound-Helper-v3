from tabnanny import check
import discord
import os
import numpy as np
import pandas as pd
import json
import helperfunctions
import constants
from dotenv import load_dotenv
import re

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# other than the tm list.json and stats.json(if we want to index it with their ID too), everything is probably easier to query

splitter = constants.message_checker_regex.format(constants.prefix)


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
with open("DATA/stats.json", encoding='utf8') as file:
    stats_dict = helperfunctions.listToDict('name',  json.load(file))
######################################################################################################


@client.event
async def on_ready():
    print(f'{client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(constants.prefix):
        query = message.content
        inputs = helperfunctions.msgSplitter(query, splitter)
        if inputs == False:  # not a message we are interested in
            return

        await message.channel.send(inputs[1])


client.run(os.getenv('tok'))


######################################CODE FOR TESTING###################################
'''x = stats_dict.get(helperfunctions.normalizeString('king ler'), False) #use this to query
print(x)
print(helperfunctions.generateStatScreen(x))


s1=";scale pokemon name"
s2=";   tmlocation focus punch"
s3="  ;     help"
s4="   ;zmove Kommomium-Z"
s5 = "; help help help help"

myreg = constants.message_checker_regex.format(constants.prefix)

print(helperfunctions.msgSplitter(s1, myreg))
print(helperfunctions.msgSplitter(s2, myreg))
print(helperfunctions.msgSplitter(s3, myreg))
print(helperfunctions.msgSplitter(s4, myreg))
'''
#########################################################################################
