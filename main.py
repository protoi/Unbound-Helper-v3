from cProfile import label
import discord
import os
import numpy as np
import pandas as pd
import json
import helperfunctions
import constants
from dotenv import load_dotenv
import re
from discord.ext import commands
from reactionmenu import ViewMenu, ViewButton

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=';', intents=(intents), help_command=None)

# other than the tm list.json and stats.json(if we want to index it with their ID too), everything is probably easier to query

splitter = constants.message_checker_regex.format(constants.prefix)
def joinstr(a):
    return str(a[0]) + " - " + str(a[1])
#region JSON DESERIALIZATION
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
    tm_name_number_mapping = dict(zip( np.char.mod('%d', np.arange(1, 121, 1)) , tmlocation_dict.keys())) #making a number string mapping for the tm dictionary

with open("DATA/tm_and_tutor.json", encoding='utf8') as file:
    tm_and_tutor_dict = helperfunctions.listToDict('name',  json.load(file))

with open("DATA/zlocation.json", encoding='utf8') as file:
    zlocation_dict = helperfunctions.listToDict('name',  json.load(file))

with open("DATA/stats.json", encoding='utf8') as file:
    stats_dict = helperfunctions.listToDict('name',  json.load(file))

with open("DATA/movedescription.json", encoding='utf8') as file:
    move_info_dict = helperfunctions.listToDict('movename',  json.load(file))

######################################################################################################
#endregion


@bot.event
async def on_ready():
    print(f'{bot.user}')
#________________________________________________________________________________________________________________
@bot.command(name='stats')
async def stats(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args)) 
    stat_element = stats_dict.get(args, False)                                       # query dictionary 
    if stat_element == False:                                                       # is key not present, display error message and break out of it
        await ctx.send(constants.invalid_text)
        return
    embedBody = constants.stat_display.format(*[*stat_element.values()])
    embedToSend = discord.Embed(
        title=stat_element.get('name',
        'place_holder_name'),
        description=embedBody)                                                      #create embed
    await ctx.send(embed = embedToSend)                                             #post embed

#________________________________________________________________________________________________________________
@bot.command(name='help')
async def help(interaction: discord.interactions):
    menu = ViewMenu(interaction, menu_type=ViewMenu.TypeEmbed, remove_buttons_on_timeout=True, all_can_click=False)

    page1 = discord.Embed(title= 'Help Page 1')                     #sets title as help page 1, don't care about rest of the message
    for index, (n,v) in enumerate(constants.help_text1):            #looping over the commant_text list for name and value pairs
        page1.add_field(                                            #adding the fields one at a time
            name=constants.prefix + n,
            value=v, 
            inline=False)
    page2 = discord.Embed(title= 'Help Page 2')                     #sets title as help page 2, don't care about rest of the message
    for index, (n,v) in enumerate(constants.help_text2):            #looping over the commant_text list for name and value pairs
        page2.add_field(                                            #adding the fields one at a time
            name=constants.prefix + n,
            value=v, 
            inline=False)
    page3 = discord.Embed(title= 'Help Page 3')                     #sets title as help page 3, don't care about rest of the message
    for index, (n,v) in enumerate(constants.help_text3):            #looping over the commant_text list for name and value pairs
        page3.add_field(                                            #adding the fields one at a time
            name=constants.prefix + n,
            value=v, 
            inline=False)
    page4 = discord.Embed(title= 'Help Page 4')                     #sets title as help page 4, don't care about rest of the message
    for index, (n,v) in enumerate(constants.help_text4):            #looping over the commant_text list for name and value pairs
        page4.add_field(                                            #adding the fields one at a time
            name=constants.prefix + n,
            value=v, 
            inline=False)
            
    menu.add_page(page1)
    menu.add_page(page2)
    menu.add_page(page3)
    menu.add_page(page4)

    menu.add_button(ViewButton.back())
    menu.add_button(ViewButton.next())                

    await menu.start()                                              #sending the embed
#________________________________________________________________________________________________________________
@bot.command(name='moves')
async def moves(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args)) 
    lvl_up_element = lvlupmoves_dict.get(args ,False)               #querying for the dictionary
    if lvl_up_element == False:                                     #if no dicitonary found, jump out of this
        await ctx.send(constants.invalid_text)                      #error message
        return
    embedTitle = lvl_up_element['name'].title()                     #setting name

    embedBody = '\n'.join( 
        ' - '.join(str(y).title() for y in x) 
        for x in lvl_up_element['lvlUpMoves'])                      #same as the for loop above OR the one liner above

    embedToSend = discord.Embed(
        title=embedTitle,
        description=embedBody) 
    await ctx.send(embed=embedToSend)                               #sending the embed
#________________________________________________________________________________________________________________
@bot.command(name='eggmoves')
async def eggmoves(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args)) 
    egg_moves_element = eggmoves_dict.get(args ,False)              #querying for the dictionary
    if egg_moves_element == False:                                  #if no dicitonary found, jump out of this
        await ctx.send(constants.invalid_text)                      #error message
        return
    embedTitle = egg_moves_element['name'].title()                  #extracting the name of the pokemon
    embedBody = "\n".join(
        x.lower() for x in 
        egg_moves_element['eggMoves'])                              #concatenating the list items
    embedToSend = discord.Embed(
        title=embedTitle,
        description=embedBody)                                      #producing an embed
    await ctx.send(embed=embedToSend)                               #sending the embed
#________________________________________________________________________________________________________________
@bot.command(name='ability')
async def ability(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args))
    abilities_element = abilities_dict.get(args, False)
            
    if abilities_element == False:                                  #if no dictionary found return and send error message
        await ctx.send(constants.invalid_text)                      #error
        return
    
    
    ability1, ability2, hiddenAbility = [str(x).lower().title()     # extracting abilites and ability descriptions for embedText
    for x in abilities_element['Ability']]
    
    ability1_desc, ability2_desc, hidden_ability_desc =  [ ability_desc_dict[helperfunctions.normalizeString(x)]['effect'] 
    for x in (ability1, ability2, hiddenAbility)]

    embedText = helperfunctions.StringFormatter(
        constants.ability_display, 
        str(ability1), 
        ability1_desc, 
        str(ability2), 
        ability2_desc, 
        str(hiddenAbility), 
        hidden_ability_desc)

    
    embedTitle = abilities_element['name'].title()                  # extract name of pokemon
    embedBody = "\n" + embedText
    embedToSend = discord.Embed(                                    #producing an embed
        title=embedTitle,
        description=embedBody)                                      
    await ctx.send(embed=embedToSend)                               #sending the embed 
#________________________________________________________________________________________________________________
@bot.command(name='tmlocation')
async def tmlocation(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args))
    q = args

    searchThis = tm_name_number_mapping.get(q, q)                   #checking if the query is present in the mapping
                                                                    #can only be possible if query was a number between 1 to 120 (inclusive)
                                                                    # obtain name of tm to search here 
    
    tmlocation_element = tmlocation_dict.get(searchThis, False)     #querying using the name now
    
    if tmlocation_element == False:                                 #if no dicitonary found, jump out of this
        await ctx.send(constants.invalid_text)          #error message
        return
    embedTitle = "TM# "+str(tmlocation_element['tmnumber'])         #extracting the name of the pokemon
    embedBody = f'''{tmlocation_element['tmname'].title()}
    {tmlocation_element['tmlocation']}'''                           #tm name + tm location in body
    embedToSend = discord.Embed(
        title=embedTitle,
        description=embedBody)                                      #producing an embed
    await ctx.send(embed=embedToSend)                   #sending the embed
#________________________________________________________________________________________________________________

bot.run(os.getenv('tok'))
