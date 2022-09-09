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
######################################################################################################
#endregion

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

        
#___________________________________________________________________________________________________________        
            
        if(inputs[1] == 'stats'):                                           #stats
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
#___________________________________________________________________________________________________________        
        elif(inputs[1] == 'help'):                                          #HELP
            embedToSend = discord.Embed(title= 'Help')                      #sets title as help, don't care about rest of the message
            for index, (n,v) in enumerate(constants.command_text):          #looping over the commant_text list for name and value pairs
                embedToSend.add_field(                                      #adding the fields one at a time
                    name=constants.prefix + n,
                    value=v, 
                    inline=False)                                           #inline commands not supported on mobile, it lets you have atmost 3 columns in your embeds
            await message.channel.send(embed = embedToSend)                 #sending the embed
#___________________________________________________________________________________________________________        

        elif(inputs[1] == 'moves'):                                         #MOVES
            if(len(inputs) < 3):                                            #checking whether message has anything after the command
                await message.channel.send(constants.invalid_text)          #invalid message
                return 
            lvl_up_element = lvlupmoves_dict.get(inputs[2] ,False)          #querying for the dictionary
            if lvl_up_element == False:                                     #if no dicitonary found, jump out of this
                await message.channel.send(constants.invalid_text)          #error message
                return
            embedTitle = lvl_up_element['name'].title()                     #setting name
            # for (n, m) in lvl_up_element['lvlUpMoves']:                   #iterating over the list of [lvl - move] pairs
            #     embedBody+= f'{str(n)} - {m.lower()}\n'                   #concatenating them
  
            # embedBody = "\n".join(joinstr(x).title() for x in lvl_up_element['lvlUpMoves'])

            embedBody = '\n'.join( 
                ' - '.join(str(y).title() for y in x) 
                for x in lvl_up_element['lvlUpMoves'])                      #same as the for loop above OR the one liner above

            embedToSend = discord.Embed(
                title=embedTitle,
                description=embedBody) 
            await message.channel.send(embed=embedToSend)                   #sending the embed
#___________________________________________________________________________________________________________        

        elif(inputs[1] == 'eggmoves'):                                      #EGGMOVES
            if(len(inputs) < 3):                                            #checking whether message has anything after the command
                await message.channel.send(constants.invalid_text)          #invalid message
                return 
            egg_moves_element = eggmoves_dict.get(inputs[2] ,False)         #querying for the dictionary
            if egg_moves_element == False:                                  #if no dicitonary found, jump out of this
                await message.channel.send(constants.invalid_text)          #error message
                return
            embedTitle = egg_moves_element['name'].title()                  #extracting the name of the pokemon
            embedBody = "\n".join(
                x.lower() for x in 
                egg_moves_element['eggMoves'])                              #concatenating the list items
            embedToSend = discord.Embed(
                title=embedTitle,
                description=embedBody)                                      #producing an embed
            await message.channel.send(embed=embedToSend)                   #sending the embed
#___________________________________________________________________________________________________________       
 
        elif(inputs[1] == 'ability'):                                       #ABILITY
            if(len(inputs) < 3):
                await message.channel.send(constants.invalid_text)          #checks for empty message
                return                                                      #error

            abilities_element = abilities_dict.get(inputs[2], False)
            
            if abilities_element == False:                                  #if no dictionary found return and send error message
                await message.channel.send(constants.invalid_text)          #error
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
            await message.channel.send(embed=embedToSend)                   #sending the embed
#___________________________________________________________________________________________________________                    
        elif(inputs[1] == 'tm'):                                            #TM
            if(len(inputs) < 3):                                            #checking whether message has anything after the command
                await message.channel.send(constants.invalid_text)          #invalid message
                return 
            
            q = inputs[2]

            searchThis = tm_name_number_mapping.get(q, q)                   #checking if the query is present in the mapping
                                                                            #can only be possible if query was a number between 1 to 120 (inclusive)
                                                                            # obtain name of tm to search here 
            
            tmlocation_element = tmlocation_dict.get(searchThis, False)     #querying using the name now
            
            if tmlocation_element == False:                                 #if no dicitonary found, jump out of this
                await message.channel.send(constants.invalid_text)          #error message
                return
            embedTitle = "TM# "+str(tmlocation_element['tmnumber'])         #extracting the name of the pokemon
            embedBody = f'''{tmlocation_element['tmname'].title()}
            {tmlocation_element['tmlocation']}'''                           #tm name + tm location in body
            embedToSend = discord.Embed(
                title=embedTitle,
                description=embedBody)                                      #producing an embed
            await message.channel.send(embed=embedToSend)                   #sending the embed
#___________________________________________________________________________________________________________       
        elif(inputs[1] == 'z' or inputs[1] == 'megastone'):                 #z crystal and megastone
            if(len(inputs) < 3):                                            #checking whether message has anything after the command
                await message.channel.send(constands.invalid_text)          #invalid message
                return
            
            if(inputs[1] == 'z'):                                           #checks for z command
                z_element = zlocation_dict.get(inputs[2], False)            #query for z crystal

                if z_element == False:                                      #does entry exist?
                    await message.channel.send(constants.invalid_text)      #if not send error
                    return
                

            elif(inputs[1] == 'megastone'):                                 #checks for megastone command
                megastone_element = megastone_dict.get(inputs[2], False)    #query for megastone

                if megastone_element == False:                              #does entry exist?
                    await message.channel.send(constants.invalid_text)      #if not send error
                    return
                
            embedTitle = z_element['name'].title()                      #extract name of z crystal
            embedBody = z_element['location']                           #extract location of z crystal
            embedToSend = discord.Embed(
                title=embedTitle,
                description=embedBody)
            await message.channel.send(embed=embedToSend)               #send embed
            return
#___________________________________________________________________________________________________________
        elif(inputs[1] == 'scale'):
            if(len(inputs) < 3):
                await message.channel.send(constants.invalid_text)
                return

            stat_element = stats_dict.get(inputs[2], False)                 # query normal stats dictionary 
            if stat_element == False:                                       # is key not present, display error message and break out of it
                await message.channel.send(constants.invalid_text)
                return
            #Get scale stats
            scaleStats = list(helperfunctions.calcScaledStats(stat_element['total'], stat_element['hp'], stat_element["attack"], stat_element['defense'], stat_element['sp_attack'], stat_element['sp_defense'], stat_element['speed']))
            #make new dictionary by combining the stats.json data with the scale stats
            scaleDict = {'number': stat_element['number'],'name': stat_element['name'],'type1': stat_element['type1'],'type2': stat_element['type2'],'generation': stat_element['generation'],'hp': scaleStats[1],'attack': scaleStats[2],'defense': scaleStats[3],'sp_attack': scaleStats[4],'sp_defense': scaleStats[5],'speed': scaleStats[6],'total': scaleStats[0]}
            
            #format embed body text
            embedBody = helperfunctions.generateStatScreen(scaleDict)
            embedToSend = discord.Embed(
                title=stat_element.get('name',
                'place_holder_name'),
                description=embedBody)                                      #create embed
            await message.channel.send(embed = embedToSend)                 #post embed
#___________________________________________________________________________________________________________
        elif(inputs[1] == 'helditem'):
            if(len(inputs) < 3):
                await message.channel.send(constants.invalid_text)
                return

            helditem_element = helditem_dict.get(inputs[2], False)
            if helditem_element == False:                                    # is key not present, display error message and break out of it
                await message.channel.send(constants.invalid_text)
                return

            embedTitle = helditem_element['itemname'].title()                #extract name of item
            embedBody = helditem_element['location']                         #extract location of item
            embedToSend = discord.Embed(
                title=embedTitle,
                description=embedBody)
            await message.channel.send(embed=embedToSend)                    #send embed
            return
#___________________________________________________________________________________________________________



client.run(os.getenv('tok'))


######################################CODE FOR TESTING###################################
# x = stats_dict.get(helperfunctions.normalizeString('galarian Darmanitan'), False) #use this to query
#print(x)
#print(helperfunctions.generateStatScreen(x))


# s1=";scale pokemon name"
# s2=";   tmlocation focus punch"
# s3="  ;     help"
# s4="   ;zmove Kommomium-Z"
# s5 = "; help help help help"
# s6 = ";ability Galarian Darmanitan"
# myreg = constants.message_checker_regex.format(constants.prefix)

#print(helperfunctions.msgSplitter(s1, myreg))
#print(helperfunctions.msgSplitter(s2, myreg))
#print(helperfunctions.msgSplitter(s3, myreg))
#print(helperfunctions.msgSplitter(s4, myreg))

#########################################################################################

