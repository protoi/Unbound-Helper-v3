##############contains the interpolated strings and the lists to be displayed.###############
########################These are the boiler plates for our embeds###########################
import re
normalize_regex = "[_\-\\ ]+"
prefix = ';'
download_link = "https://www.mediafire.com/file/brvvppywnxhmsdb/Pokemon+Unbound+Official+Patch+2.0+.zip/file"
stat_display = 'HP:{}\nAttack:{}\nDefense:{}\nSp.Attack:{}\nSp.Def:{}\nSpeed:{}'
ability_display = 'Ability 1:{}\nAbility 2:{}\nHidden Ability:{}'
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

caps_display = "**Gym 1:** 20\n**Gym 2:** 26\n**Gym 3:** 32\n**Gym 4:** 36\n**Maxima:** 40\n**Gym 5:** 45\n**Gym 6:** 52\n**Gym 7:** 57\n**Gym 8:** 61\n**Elite 4:** 75"
invalid_text = "Sorry, invalid input!"
vanilla_text = ["Vanilla",
                "• More in line with official game difficulty nowadays. Play this if you like over leveling or just want to play a game without worrying too much about the battles. My 8-year old brother beat this several times using Ash's teams (and remember, Ash rarely evolved his Pokemon). EV training is not required."]
difficult_text = ["Difficult",
                  "• Difficult: You're looking for something slightly harder than normal Pokémon games, and don't mind losing boss battles once or twice to force you to rethink your strategy with the same team. EV training is not required."]
expert_text = ["Expert",
               "• Expert: If you're running a fully EV trained team, this is probably going to be as hard as Difficult early on. You also probably won't need to change up your team in between major battles. Late game will get harder, though, but still nowhere near as hard as Insane"]
insane_text = ["Insane",
               "Insane: This should be the hardest hack you've ever played. Period. Items can't be used in Trainer battles, and bosses all have a team with competitive movesets and full EVs. If you're ready to rage quit after the first Gym, this difficulty is NOT for you. It was designed to be inherently unfun for most players."]
shiny_odd_text = "Regular Shiny Odds: 1/4096\nShiny Odds with Shiny Charm: 1/1365\nMasuda Method: 1/683\nMasuda Method + Shiny Charm: 1/512\nMax Search Levels + Encounter at Chain Length 100 + Shiny Charm: 2.039%\nMax Search Levels + Encounter at Chain Length 100: 0.68%\nMax Search Levels + Shiny Charm: 0.478%\nMax Search Levels: 0.159%\nScammer Method: 100%"
pick_up_image_source = ["Drop Table(thank you `SevenK`):",
                        "https://cdn.discordapp.com/attachments/810125662937284619/916670464712142898/2.0Pickup.png"]
kbt_image_source = ["K.B.T tutor list(thank you `fox appreciation`, `SevenK`, LuckyHour and Falkyri3): ",
                    "https://cdn.discordapp.com/attachments/792456927073796117/964141023267786794/tutor_infographic.png"]

command_text = [
    ["moves",
     "Syntax: `;moves <pokemon_name>`\nDisplays the level up moves of a pokemon"],
    ["eggmoves",
     "Syntax: `;eggmoves <pokemon_name>`\nDisplays the egg moves of a pokemon"],
    ["ability",
     "Syntax: `;ability <pokemon_name>`\nDisplays the abilities of the Pokemon, thank SevenK for this :pleading_face:"],
    ["tm",
     "Syntax: `;tm <tm_number>` OR `;tm <tm_name>`\nDisplays the location of the TM"],
    ["location",
     "Syntax: `;location <pokemon_name>`\nDisplays the location(s) of a pokemon(thank you Spectre and SevenK for the pokemon guide)"],
    ["megastone",
     "Syntax: `;megastone <megastone_name>`\nDislays the mega stone location."],
    ["z",
     "Syntax: `;z <z move_name>`\nDislays the Z move location."],
    ["helditem",
     "Syntax: `;helditem <item name>`\nDislays the held item location(may not have everything you want) Thankyou Sparrow and SevenK🥺🥺🥺."],
    ["difficulty",
     "Syntax: `;difficulty`\nDisplays the difficulty summary"],
    ["statmods",
     "Syntax: `;statmods`\nDisplays the bottle cap lady's schedue"],
    ["shinyodd",
     "Syntax: `;shinyodd` OR `;shiny`\nDisplays the odds of getting a shiny"],
    ["pickup",
     "Syntax: `;pickup` OR `;pick`\nDisplays the pickup drop table"],
    ["kbt",
     "Syntax: `;kbt` OR `;KBT`\nDisplays the KBT tutor list"],
    ["breeding",
     "Syntax: `;breeding`\nDisplays the incenses required to breed certain pokemons"],
    ["caps",
     "Syntax: `;caps` OR `;lvlcaps`\nDislays the levels caps of Gym Leaders."],
    ["download",
     "Syntax: `;download`\nThe URL to download the latest patch to Pokemon Unbound."],
    ["league",
     "Syntax: `;league`\nGym Leader and Elite 4 teams for the Insane difficulty."],
    ["tutor",
     "Syntax: `;tutor <pokemon_name> `\nshows tutor compatibility, thanks dave99 for the lists!!"],
    ["learntm",
     "Syntax: `;learntm <pokemon_name>`\nshows tm compatibility, thanks dave99 again!!!!"],
    ["scale",
     "Syntax: `;scale <pokemon_name>`\nscalemon stats"]
]
