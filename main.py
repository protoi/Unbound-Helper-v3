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
@bot.command(name='stats')                                          #STATS
async def stats(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args)) 
    stat_element = stats_dict.get(args, False)                      #query dictionary 
    if stat_element == False:                                       #is key not present, display error message and break out of it
        await ctx.send(constants.invalid_text)
        return
    embedBody = constants.stat_display.format(*[*stat_element.values()])
    embedToSend = discord.Embed(
        title=stat_element.get('name',
        'place_holder_name'),
        description=embedBody)                                      #create embed
    await ctx.send(embed = embedToSend)                             #post embed

#________________________________________________________________________________________________________________
@bot.command(name='help')                                           #HELP
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
@bot.command(name='moves')                                          #MOVES
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
@bot.command(name='eggmoves')                                       #EGGMOVES
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
@bot.command(name='ability')                                        #ABILITY
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
@bot.command(name='tmlocation')                                     #TMLOCATION
async def tmlocation(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args))
    q = args

    searchThis = tm_name_number_mapping.get(q, q)                   #checking if the query is present in the mapping
                                                                    #can only be possible if query was a number between 1 to 120 (inclusive)
                                                                    # obtain name of tm to search here 
    
    tmlocation_element = tmlocation_dict.get(searchThis, False)     #querying using the name now
    
    if tmlocation_element == False:                                 #if no dicitonary found, jump out of this
        await ctx.send(constants.invalid_text)                      #error message
        return
        
    embedTitle = "TM# "+str(tmlocation_element['tmnumber'])         #extracting the name of the pokemon
    embedBody = f'''{tmlocation_element['tmname'].title()}
    {tmlocation_element['tmlocation']}'''                           #tm name + tm location in body
    embedToSend = discord.Embed(
        title=embedTitle,
        description=embedBody)                                      #producing an embed
    await ctx.send(embed=embedToSend)                               #sending the embed
#________________________________________________________________________________________________________________
@bot.command(name='z')                                              #Z
async def z(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args))

    z_element = zlocation_dict.get(args, False)                     #query for z crystal

    if z_element == False:                                          #does entry exist?
        await ctx.send(constants.invalid_text)                      #if not send error
        return

    embedTitle = z_element['name'].title()                          #extract name of z crystal
    embedBody = z_element['location']                               #extract location of z crystal
    embedToSend = discord.Embed(
        title=embedTitle,
        description=embedBody)
    await ctx.send(embed=embedToSend)                               #send embed
#________________________________________________________________________________________________________________
@bot.command(name='megastone')                                      #MEGASTONE
async def megastone(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args))

    megastone_element = megastone_dict.get(args, False)             #query for megastone

    if megastone_element == False:                                  #does entry exist?
        await ctx.send(constants.invalid_text)                      #if not send error
        return

    embedTitle = megastone_element['name'].title()                  #extract name of megastone
    embedBody = megastone_element['location']                       #extract location of megastone
    embedToSend = discord.Embed(
        title=embedTitle,
        description=embedBody)
    await ctx.send(embed=embedToSend)                               #send embed
#________________________________________________________________________________________________________________
@bot.command(name='scale')                                          #SCALE
async def scale(xtc, *args):
    args = helperfunctions.normalizeString(' '.join(args))

    stat_element = stats_dict.get(args, False)                      #query normal stats dictionary 
    if stat_element == False:                                       #is key not present, display error message and break out of it
        await ctx.send(constants.invalid_text)
        return
    
    standard_data = [*stat_element.values()][:5]                    #data that doesnt change with scalemons (name, type, generation)
    un_scaled_data = [*stat_element.values()][5:]                   #data that changes in scalemons (stats)
    scaled_data  = helperfunctions.calcScaledStats(un_scaled_data)  #returns a scaled list of [hp, attack, def, spatt, spdef, speed, BST]

    combined_list  = standard_data + [                              #making a new list from the scalemons stats string and standard data 
        constants.just_stats.format(*scaled_data)
        ]
    embedBody =  constants.for_scalemons.format(*combined_list)     #formatting for_scalemons with the created list

    embedToSend = discord.Embed(
        title=stat_element.get('name',
        'place_holder_name'),
        description=embedBody)                                      #create embed

    embedToSend.set_footer(text = '''Only fully evolved
Pokemon including 
mega evolutions
(except Shedinja)
get scaled in
Scalemons Story Mode''')                                            #setting a footer
    await ctx.send(embed = embedToSend)                             #post embed
#________________________________________________________________________________________________________________
@bot.command(name='helditem')                                       #HELDITEM
async def helditem(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args))

    helditem_element = helditem_dict.get(args, False)
    if helditem_element == False:                                   #is key not present, display error message and break out of it
        await ctx.send(constants.invalid_text + 
        " What you are looking for might not be an item that can be obtained from wild pokemons")
        return

    embedTitle = helditem_element['itemname'].title()               #extract name of item
    embedBody = helditem_element['location']                        #extract location of item
    embedToSend = discord.Embed(
        title=embedTitle,
        description=embedBody)
    await ctx.send(embed=embedToSend)                               #send embed
    return
#________________________________________________________________________________________________________________
@bot.command(name='location')                                       #LOCATION
async def location(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args))

    pokelocation_element = pokelocation_dict.get(args, False)
    if pokelocation_element == False:                               #is key not present, display error message and break out of it
        await ctx.send(constants.invalid_text)
        return

    embedTitle = pokelocation_element['name'].title()               #extract name of pokemon
    embedBody = pokelocation_element['location']                    #extract location of pokemon
    embedToSend = discord.Embed(
        title=embedTitle,
        description=embedBody)
    await ctx.send(embed=embedToSend)                               #send embed
    return
#________________________________________________________________________________________________________________
@bot.command(name='difficulty')                                     #DIFFICULTY
async def difficulty(ctx):

    embedToSend = discord.Embed(title= '**Which difficulty should I pick:**') 
    for index, (n,v) in enumerate(constants.difficulty_text):       #looping over the commant_text list for name and value pairs
        embedToSend.add_field(                                      #adding the fields one at a time
            name=n,
            value=v, 
            inline=False)                                           #inline commands not supported on mobile, it lets you have atmost 3 columns in your embeds
    await ctx.send(embed = embedToSend)                             #sending the embed
    return
#________________________________________________________________________________________________________________
@bot.command(name='shinyodd')                                       #SHINYODD & SHINY
async def shinyodd(ctx):

    embedTitle = '**Shiny Odds:**'
    embedBody = constants.shiny_odd_text
    embedToSend = discord.Embed(
        title=embedTitle,
        description=embedBody
    )
    await ctx.send(embed=embedToSend)                               #send embed
    return
@bot.command(name='shiny')
async def shiny(ctx):

    embedTitle = '**Shiny Odds:**'
    embedBody = constants.shiny_odd_text
    embedToSend = discord.Embed(
        title=embedTitle,
        description=embedBody
    )
    await ctx.send(embed=embedToSend)                               #send embed
    return
#________________________________________________________________________________________________________________
@bot.command(name='pickup')                                         #PICKUP
async def pickup(ctx):

    embedToSend = discord.Embed(title=constants.pick_up_image_source[0]) #creates embed
    embedToSend.set_image(url=constants.pick_up_image_source[1])    #adds image to embed
    await ctx.send(embed=embedToSend)                               #send embed
    return
#________________________________________________________________________________________________________________
@bot.command(name='kbt')                                            #KBT
async def kbt(ctx):

    embedToSend = discord.Embed(title=constants.kbt_image_source[0])#creates embed
    embedToSend.set_image(url=constants.kbt_image_source[1])        #adds image to embed
    await ctx.send(embed=embedToSend)                               #send embed
    return
#________________________________________________________________________________________________________________
@bot.command(name='breeding')                                       #BREEDING
async def breeding(ctx):

    embedToSend = discord.Embed(title= '**Extreme Hyperosmia Breeding Help:**') 
    for index, (n,v) in enumerate(constants.breeding_display):      #looping over the commant_text list for name and value pairs
        embedToSend.add_field(                                      #adding the fields one at a time
            name=n,
            value=v, 
            inline=False)                                           #inline commands not supported on mobile, it lets you have atmost 3 columns in your embeds
    await ctx.send(embed = embedToSend)                             #sending the embed
    return
#________________________________________________________________________________________________________________
@bot.command(name='caps')                                           #CAPS & LVLCAPS
async def caps(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args))

    if args == '':
        embedBody  = constants.caps_template.format(*constants.other_caps)
        embedTitle  = '**Level Caps: Difficult+**'
    if args == 'vanilla':
        embedBody  = constants.caps_template.format(*constants.vanilla_caps)
        embedTitle = '**Level Caps: Vanilla**'
    else:                                                           #break out of it if gibberish 

        await ctx.send(constants.invalid_text)
        return

    embedToSend = discord.Embed(
        title=embedTitle,
        description=embedBody
    )
    await ctx.send(embed=embedToSend)                               #send embed
    return 
@bot.command(name='lvlcaps')                                        
async def lvlcaps(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args))

    if args == '':
        embedBody  = constants.caps_template.format(*constants.other_caps)
        embedTitle  = '**Level Caps: Difficult+**'
    if args == 'vanilla':
        embedBody  = constants.caps_template.format(*constants.vanilla_caps)
        embedTitle = '**Level Caps: Vanilla**'
    else:                                                           #break out of it if gibberish 

        await ctx.send(constants.invalid_text)
        return

    embedToSend = discord.Embed(
        title=embedTitle,
        description=embedBody
    )
    await ctx.send(embed=embedToSend)                               #send embed
    return 
#________________________________________________________________________________________________________________
@bot.command(name='download')                                       #DOWNLOAD
async def download(ctx):

    embedToSend = discord.Embed(
        title='**Pokemon Unbound Official Patch:**',
        description='[Pokemon Unbound Official Patch](https://www.mediafire.com/file/brvvppywnxhmsdb/Pokemon+Unbound+Official+Patch+2.0+.zip/file)'
    ) 
    await ctx.send(embed=embedToSend)                               #send embed
    return
#________________________________________________________________________________________________________________
@bot.command(name='docs')                                           #DOCS
async def docs(ctx):

    embedTitle = '**Offical Unbound Docs:**'                        #extracting the name of the pokemon
    embedBody = "\n".join(
        x for x in 
        constants.docs_text)                                        #concatenating the list items

    embedToSend = discord.Embed(
        title=embedTitle,
        description=embedBody)                                      #producing an embed
    await ctx.send(embed=embedToSend)
    return  
#________________________________________________________________________________________________________________
@bot.command(name='learntm')                                        #LEARNTM
async def learntm(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args))

    tm_element = tm_and_tutor_dict.get(args ,False)                 #querying for the dictionary

    if tm_element == False:                                         #if no dicitonary found, jump out of this
        await ctx.send(constants.invalid_text)                      #error message
        return
    embedTitle = "TM's compatible with "
    embedBody = ", ".join(
        x.title() for x in 
        tm_element.get('tmMoves', "")
    )
    embedTitle += tm_element['name'].title()                        #extracting the name of the pokemon
    
    embedToSend = discord.Embed(
        title=embedTitle,
        description=embedBody)                                      #producing an embed
    await ctx.send(embed=embedToSend)                               #sending the embed
#________________________________________________________________________________________________________________
@bot.command(name='tutor')                                          #TUTOR
async def tutor(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args))

    tutor_element = tm_and_tutor_dict.get(args ,False)              #querying for the dictionary
    if tutor_element == False:                                      #if no dicitonary found, jump out of this
        await ctx.send(constants.invalid_text)                      #error message
        return
    embedTitle = "Tutor moves learnt by "
    embedBody = ", ".join(
        x.title() for x in 
        tutor_element.get('tmMoves', "")
    )
    embedTitle += tutor_element['name'].title()                     #extracting the name of the pokemon
    
    embedToSend = discord.Embed(
        title=embedTitle,
        description=embedBody)                                      #producing an embed
    await ctx.send(embed=embedToSend)                               #sending the embed
#________________________________________________________________________________________________________________
@bot.command(name='moveinfo')                                       #MOVEINFO
async def moveinfo(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args))

    move_info_element = move_info_dict.get(args ,False)             #querying for the dictionary
    if move_info_element == False:                                  #if no dicitonary found, jump out of this
        await ctx.send(constants.invalid_text)                      #error message
        return
    embedTitle = move_info_element['movename'].title()              #setting name
    
    embedBody = constants.move_info_display.format(
        *[*(move_info_element.values())][1:])                       #removing the first element, it's the name being displayed in the title
    
    embedToSend = discord.Embed(
        title=embedTitle,
        description=embedBody) 
    await ctx.send(embed=embedToSend)                               #sending the embed
#________________________________________________________________________________________________________________
bot.run(os.getenv('tok'))