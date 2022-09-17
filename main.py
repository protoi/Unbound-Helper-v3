from cProfile import label
from math import ceil
import discord
import os
import numpy as np
import json
import helperfunctions
import constants
from dotenv import load_dotenv
from discord.ext import commands
from reactionmenu import ViewMenu, ViewButton

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=constants.prefix, intents=(intents), help_command=None)

# other than the tm list.json and stats.json(if we want to index it with their ID too), everything is probably easier to query

splitter = constants.message_checker_regex.format(constants.prefix)

maxEntriesPerPage = 5
numOfPages = ceil(len(constants.command_text) / maxEntriesPerPage)

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

with open("DATA/Learnsets.json", encoding='utf8') as file:
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

with open("DATA/Base_Stats.json", encoding='utf8') as file:
    base_stats_dict = helperfunctions.listToDict('name',  json.load(file))

######################################################################################################
#endregion


@bot.event
async def on_ready():
    print(f'{bot.user}')

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"uh oh, something went wrong. Error: {error}")                               #sending the embed


#________________________________________________________________________________________________________________
@bot.command(name='help')                                           #HELP
async def help(interaction: discord.interactions):
    menu = ViewMenu(interaction, menu_type=ViewMenu.TypeEmbed, remove_buttons_on_timeout=True, all_can_click=False)

    pages = []

    for i in range(0, numOfPages):                                  #Producing the pages
        pages.append(discord.Embed(title = f"Help Page #{i+1}"))
        
        for j in range(0, maxEntriesPerPage):                       #adding information to the pages
            currentIndex =  j + i * maxEntriesPerPage
            if currentIndex == len(constants.command_text):
                break
            pages[i].add_field(
                name= constants.prefix + constants.command_text[currentIndex][0],
                value = constants.command_text[currentIndex][1],
                inline = False
            )
            
    for p in pages:
        menu.add_page(p)
            
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
@bot.command(name='tmlocation', aliases=['tm'])                     #TMLOCATION
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
@bot.command(name='shiny', aliases=['shinyodd'])                    #SHINYODD & SHINY
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
@bot.command(name='caps', aliases=['lvlcaps'])                      #CAPS & LVLCAPS
async def caps(ctx, *args):
    args = helperfunctions.normalizeString(' '.join(args))

    if args == 'vanilla' or args == 'v':
        embedBody  = constants.caps_template.format(*constants.vanilla_caps)
        embedTitle = '**Level Caps: Vanilla**'
    else:
        embedBody  = constants.caps_template.format(*constants.other_caps)
        embedTitle  = '**Level Caps: Difficult+**'
    
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

@bot.command(name='stats')                                          #STATS AND SCALEMONS
async def stats(interaction: discord.interactions, *args ):
    scalemonFlag=False                                              #setting the scalemon flag to be false initially
    
    if len(args) != 0 and helperfunctions.normalizeString(args[0]) == 'scale':
        scalemonFlag = True                                         #setting it to true if user wants scaled stats
    
    if scalemonFlag:
        args = helperfunctions.normalizeString(' '.join(args[1:])) 
    else:
        args = helperfunctions.normalizeString(' '.join(args[0:])) 

    base_stat_element = base_stats_dict.get(args, False)            #query dictionary 
    if base_stat_element == False:                                  #is key not present, display error message and break out of it
        await interaction.send(content = constants.invalid_text)
        return
    
    s,t,c,e,i,b,a,ch = helperfunctions.getComplexStats(base_stat_element['stats'], scalemonFlag)


    stat_menu = ViewMenu(interaction, menu_type=ViewMenu.TypeEmbed, remove_buttons_on_timeout=True, all_can_click=False)

    if scalemonFlag:
        simple_page = discord.Embed(title= "Scalemon " + base_stat_element['name'])
        simple_page.set_footer(text=constants.scalemon_warning)
        complex_page = discord.Embed(title = "Scalemon " + base_stat_element['name'])
        complex_page.set_footer(text = constants.scalemon_warning)

    else:
        simple_page = discord.Embed(title= base_stat_element['name'])
        complex_page = discord.Embed(title = base_stat_element['name'])

    simple_page = helperfunctions.addFieldToEmbeds(simple_page, [t, s, a], ["Type", "Stats", "Abilities"])
    complex_page = helperfunctions.addFieldToEmbeds(complex_page, [b, i, e, c, ch], [
    "Breeding Information",
    "Items",
    "EV Yields",
    "Catch Information",
    "Miscellaneous"])

    stat_menu.add_page(simple_page)
    stat_menu.add_page(complex_page)
            
    stat_menu.add_button(ViewButton.next())

    await stat_menu.start() #posting the menu


bot.run(os.getenv('tok'))