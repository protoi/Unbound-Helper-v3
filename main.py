from dataclasses import field, fields
from dis import disco
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
        embedToSend = None
        query = message.content
        inputs = helperfunctions.msgSplitter(query, splitter)
        if inputs == False:  # not a message we are interested in
            return
            
        if(inputs[1] == 'pokedata'):                                        #POKEDATA
            if(len(inputs) < 3):                                            # check if there is a key associated with the command
                await message.channel.send(constants.invalid_text)          #error message
                return
            stat_element = stats_dict.get(inputs[2], False)                 # query dictionary 
            if stat_element == False:                                       # is key not present, display error message and break out of it
                await message.channel.send(constants.invalid_text)
                return
            embedBody = helperfunctions.generateStatScreen(stat_element)    #obtain formatted string
            embedToSend = discord.Embed(
                title=stat_element.get('name',
                'place_holder_name'),
                description=embedBody)                                      #create embed
            await message.channel.send(embed = embedToSend)                 #post embed
        
        elif(inputs[1] == 'help'):                                          #HELP
            embedToSend = discord.Embed(title= 'Help')                      #sets title as help, don't care about rest of the message
            for index, (n,v) in enumerate(constants.command_text):          #looping over the commant_text list for name and value pairs
                embedToSend.add_field(                                      #adding the fields one at a time
                    name=constants.prefix + n,
                    value=v, 
                    inline=False)                                           #inline commands not supported on mobile, it lets you have atmost 3 columns in your embeds
            await message.channel.send(embed = embedToSend)                 #sending the embed

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
