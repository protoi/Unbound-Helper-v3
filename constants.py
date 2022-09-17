from math import ceil
##############contains the interpolated strings and the lists to be displayed.###############
########################These are the boiler plates for the embeds###########################

normalize_regex = "[_\-\\\. ]+"

message_checker_regex = "[ ]*({})[ ]*([a-zA-Z]+)[ ]*(.*)"

prefix = ';'

other_caps = [20, 26, 32, 36, 40, 45, 52, 57, 61, 75]

vanilla_caps = [15, 22, 29, 33, 37, 43, 51, 55, 60, 66]

stat_display = '''Dex Number: {}
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

just_stats = '''HP: {}
Attack: {}
Defense: {}
Sp.Attack: {}
Sp.Def: {}
Speed: {}

Total: {}
'''

for_scalemons = '''Dex Number: {}
Name: {}
Type: {} {}
Generation: {}

{}
'''

ability_display = '''__Ability 1__: **{}**
{}

__Ability 2__: **{}**
{}

__Hidden Ability__: **{}**
{}'''

breeding_display = [
    ["Wynaut:", "Breed Wobbuffet  with Lax Incense."],
    ["Munchlax:", "Breed Snorlax with Full Incense."],
    ["Chingling:", "Breed Chimecho with Pure Incense."],
    ["Mime Jr:", "Breed Mr. Mime with Odd Incense."],
    ["Bonsly:", "Breed Sudowoodo with Rock Incense."],
    ["Mantyke:", "Breed Mantine with Wave Incense."],
    ["Azuril:", "Breed Azumarill with Sea Incense."],
    ["Budew:", "Breed Roserade/Roselia with Rose Incense."],
    ["Happiny:", "Breed Chansey/Blissey with Luck Incense."]
]

caps_template = '''**Gym 1:** {}
**Gym 2:** {}
**Gym 3:** {}
**Gym 4:** {}
**Maxima:** {}
**Gym 5:** {}
**Gym 6:** {}
**Gym 7:** {}
**Gym 8:** {}
**Elite 4:** {}'''

invalid_text = "Sorry, invalid input!"

difficulty_text = [
    ["Vanilla",
        "• Vanilla: More in line with official game difficulty nowadays. Play this if you like over leveling or just want to play a game without worrying too much about the battles. My 8-year old brother beat this several times using Ash's teams (and remember, Ash rarely evolved his Pokemon). EV training is not required."],
    ["Difficult",
        "• Difficult: You're looking for something slightly harder than normal Pokémon games, and don't mind losing boss battles once or twice to force you to rethink your strategy with the same team. EV training is not required."],
    ["Expert",
        "• Expert: If you're running a fully EV trained team, this is probably going to be as hard as Difficult early on. You also probably won't need to change up your team in between major battles. Late game will get harder, though, but still nowhere near as hard as Insane"],
    ["Insane",
        "• Insane: This should be the hardest hack you've ever played. Period. Items can't be used in Trainer battles, and bosses all have a team with competitive movesets and full EVs. If you're ready to rage quit after the first Gym, this difficulty is NOT for you. It was designed to be inherently unfun for most players."]
]

docs_text = [
    '[General Guide (Pokemon, Items, Missions, etc.) ](https://docs.google.com/spreadsheets/d/1LFSBZuPDtJrwAz7t6ZkJ-il4j8M3qCdaKLNe6EZdPmQ/edit#gid=693940475)' + '(Credits to The Spectre)',
    '[Location Guide ](https://docs.google.com/spreadsheets/d/1PyGm-yrit5Ow6cns2tBA9VEMwLVMzn3YhDRipABjLUM/edit?usp=drivesdk)' + '(Credits to SevenK)',
    '[Mission Guide+ (Daily Events, Key Items, Berry Blender, etc.) ](https://docs.google.com/spreadsheets/d/1-sQWHzIbLw2hSLfrUILg9prcbdDN57zefXhNF7Bx2PY/edit?usp=sharing)' + '(Credits to SevenK)',
    '[Pokedex ](https://unbound.ashencone.com/)' + '(Credits to Sounak9434)',
    '[TM Compatibility](https://github.com/Skeli789/Dynamic-Pokemon-Expansion/tree/Unbound/src/tm_compatibility)',
    '[Tutor Compatibility](https://github.com/Skeli789/Dynamic-Pokemon-Expansion/tree/Unbound/src/tutor_compatibility)',
    '[Evolutions](https://raw.githubusercontent.com/Skeli789/Dynamic-Pokemon-Expansion/Unbound/src/Evolution%20Table.c)',
    '[Raid Drops Guide](https://docs.google.com/spreadsheets/d/1rf6ch14TKmAuWDAR0uJbDTirnC14YVUXNFFN0yWxs-8/edit?usp=drivesdk)',
    '[Trainers ](https://docs.google.com/spreadsheets/d/1Ha06sD9mKw5yXXT2icVZjVQapcArU5C5gLEvA-hkq9o/)' +
    '(Credits to SkiDY)'
]

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
    ["tmlocation",
     '''Syntax: `;tmlocation <tm_number>` OR `;tmlocation <tm_name>`
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
    ["tutor",
     '''Syntax: `;tutor <pokemon_name> `
     shows tutor compatibility, thanks dave99 for the lists!!'''],
    ["learntm",
     '''Syntax: `;learntm <pokemon_name>`
     shows tm compatibility, thanks dave99 again!!!!'''],
    ["scale",
     '''Syntax: `;scale <pokemon_name>`
     scalemon stats'''],
    ["stats",
     '''Syntax: `;stats <pokemon_name>`
     normal stats'''],
    ["docs",
     '''Syntax: `;docs`
     shows links to the docs''']
]

move_info_display = '''__Description__: {}
__Effect__: {}
__Power__: {}
__Type__: {}
__Accuracy__: {}
__PP__: {}
__Effect Accuracy__: {}
__Target__: {}
__Priority__: {}
__Info__: {}
'''

scalemon_warning = '''Only fully evolved
Pokemon including 
mega evolutions
(except Shedinja)
get scaled in
Scalemons Story Mode'''

pokemon_stat_template = '''
HP: {}
Attack: {}
Defense: {}
SpAttack: {}
SpDefense: {}
Speed: {}

BST: {}
'''

pokemon_type_template = '''{}'''

pokemon_capture_template = '''
Catch Rate: {}
EXP Yield: {}
'''

pokemon_ev_yields_template = '''
HP: {}
Attack: {}
Defense: {}
SpAttack: {}
SpDefense: {}
Speed: {}
'''

pokemon_item_template = '''
Item 1: {}
Item 2: {}
'''

pokemon_breeding_template = '''
Gender Ratio: {}
egg Cycles: {}
egg Group: {}
'''

pokemon_ability_template = '''
Ability 1: {}
Ability 2: {}

Hidden Ability: {}
'''

pokemon_characteristics_template = '''
Friendship: {}
Growth Rate: {}
'''

maxEntriesPerPageHelp = 5                       #max entries we want in the ;help menu section

numOfPagesHelp = ceil(len(command_text) / maxEntriesPerPageHelp) #number of pages needed to accomodate this many page elements

maxEntriesPerPageGifts = 6                       #max entries we want in the ;gifts menu section
