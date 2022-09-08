##############contains the interpolated strings and the lists to be displayed.###############
########################These are the boiler plates for the embeds###########################

normalize_regex = "[_\-\\ ]+"

message_checker_regex= "[ ]*({})[ ]*([a-zA-Z]+)[ ]*(.*)"

prefix = ';'

stat_display='''Number: {}
Name: {}
Type: {} {}
Generation: {}
HP: {}
Attack: {}
Defense: {}
Sp.Attack: {}
Sp.Def: {}
Speed: {}
Total: {}
'''

download_link = "https://www.mediafire.com/file/brvvppywnxhmsdb/Pokemon+Unbound+Official+Patch+2.0+.zip/file"

stat_display_relegated = '''HP:{}
Attack:{}
Defense:{}
Sp.Attack:{}
Sp.Def:{}
Speed:{}'''

ability_display = '''Ability 1:{} 
{}
Ability 2:{} 
{}
 Hidden Ability:{}
{}'''

breeding_display = [
    ["Wynaut:", "Breed Wobuffet  with Lax Incense."],
    ["Munchlax:", "Breed Snorlax with Full Incense."],
    ["Chingling:", "Breed Chimecho with Pure Incense."],
    ["Mime Jr:", "Breed Mr. Mime with Odd Incense."],
    ["Bonsly:", "Breed Sudowoodo with Rock Incense."],
    ["Mantyke:", "Breed Mantine with Wave Incense."],
    ["Azuril:", "Breed Azumarill with Sea Incense."],
    ["Budew:", "Breed Roserade/Roselia with Rose Incense."],
    ["Happiny:", "Breed Chansey/Blissey with Luck Incense."]
]

caps_display = '''**Gym 1:** 20
**Gym 2:** 26
**Gym 3:** 32
**Gym 4:** 36
**Maxima:** 40
**Gym 5:** 45
**Gym 6:** 52
**Gym 7:** 57
**Gym 8:** 61
**Elite 4:** 75'''


invalid_text = "Sorry, invalid input!"

vanilla_text = ["Vanilla",
                "• More in line with official game difficulty nowadays. Play this if you like over leveling or just want to play a game without worrying too much about the battles. My 8-year old brother beat this several times using Ash's teams (and remember, Ash rarely evolved his Pokemon). EV training is not required."]
difficult_text = ["Difficult",
                  "• Difficult: You're looking for something slightly harder than normal Pokémon games, and don't mind losing boss battles once or twice to force you to rethink your strategy with the same team. EV training is not required."]
expert_text = ["Expert",
               "• Expert: If you're running a fully EV trained team, this is probably going to be as hard as Difficult early on. You also probably won't need to change up your team in between major battles. Late game will get harder, though, but still nowhere near as hard as Insane"]
insane_text = ["Insane",
               "Insane: This should be the hardest hack you've ever played. Period. Items can't be used in Trainer battles, and bosses all have a team with competitive movesets and full EVs. If you're ready to rage quit after the first Gym, this difficulty is NOT for you. It was designed to be inherently unfun for most players."]

shiny_odd_text = '''Regular Shiny Odds: 1/4096
Shiny Odds with Shiny Charm: 1/1365
Masuda Method: 1/683
Masuda Method + Shiny Charm: 1/512
Max Search Levels + Encounter at Chain Length 100 + Shiny Charm: 2.039%
Max Search Levels + Encounter at Chain Length 100: 0.68%
Max Search Levels + Shiny Charm: 0.478%
Max Search Levels: 0.159%
Scammer Method: 100%'''

pick_up_image_source = ["Drop Table(thank you `SevenK`):",
                        "https://cdn.discordapp.com/attachments/810125662937284619/916670464712142898/2.0Pickup.png"]

kbt_image_source = ["K.B.T tutor list(thank you `fox appreciation`, `SevenK`, LuckyHour and Falkyri3): ",
                    "https://cdn.discordapp.com/attachments/792456927073796117/964141023267786794/tutor_infographic.png"]

command_text = [
    ["moves",
     '''Syntax: `;moves <pokemon_name>`
     Displays the level up moves of a pokemon'''],
    ["eggmoves",
     '''Syntax: `;eggmoves <pokemon_name>`
     Displays the egg moves of a pokemon'''],
    ["ability",
     '''Syntax: `;ability <pokemon_name>`
     Displays the abilities of the Pokemon, thank SevenK for this :pleading_face:'''],
    ["tm",
     '''Syntax: `;tm <tm_number>` OR `;tm <tm_name>`
     Displays the location of the TM'''],
    ["location",
     '''Syntax: `;location <pokemon_name>`
     Displays the location(s) of a pokemon(thank you Spectre and SevenK for the pokemon guide)'''],
    ["megastone",
     '''Syntax: `;megastone <megastone_name>`
     Dislays the mega stone location.'''],
    ["z",
     '''Syntax: `;z <z move_name>`
     Dislays the Z move location.'''],
    ["helditem",
     '''Syntax: `;helditem <item name>`
     Dislays the held item location(may not have everything you want) Thankyou Sparrow and SevenK🥺🥺🥺.'''],
    ["difficulty",
     '''Syntax: `;difficulty`
     Displays the difficulty summary'''],
    ["statmods",
     '''Syntax: `;statmods`
     Displays the bottle cap lady's schedue'''],
    ["shinyodd",
     '''Syntax: `;shinyodd` OR `;shiny`
     Displays the odds of getting a shiny'''],
    ["pickup",
     '''Syntax: `;pickup` OR `;pick`
     Displays the pickup drop table'''],
    ["kbt",
     '''Syntax: `;kbt` OR `;KBT`
     Displays the KBT tutor list'''],
    ["breeding",
     '''Syntax: `;breeding`
     Displays the incenses required to breed certain pokemons'''],
    ["caps",
     '''Syntax: `;caps` OR `;lvlcaps`
     Dislays the levels caps of Gym Leaders.'''],
    ["download",
     '''Syntax: `;download`
     The URL to download the latest patch to Pokemon Unbound.'''],
    ["league",
     '''Syntax: `;league`
     Gym Leader and Elite 4 teams for the Insane difficulty.'''],
    ["tutor",
     '''Syntax: `;tutor <pokemon_name> `
     shows tutor compatibility, thanks dave99 for the lists!!'''],
    ["learntm",
     '''Syntax: `;learntm <pokemon_name>`
     shows tm compatibility, thanks dave99 again!!!!'''],
    ["scale",
     '''Syntax: `;scale <pokemon_name>`
     scalemon stats''']
]
