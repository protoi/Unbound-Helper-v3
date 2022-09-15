from ast import Try
import re
import json
level = open("extractor\stats\Base_Stats.c", "r")

count = 0
overAllStats = []  # overAllStats.append(temp_dict)
temp_name = ""
temp_stats = {}
# temp_dict['name'] = temp_name, temp_dict['stats'] = temp_stats
temp_dict = {}


def calcFem(percent): return min(254, ((percent * 255) / 100))


REGEX_FIRST_LINE = r"[ ]*\[[ ]*SPECIES_([\w]*)\]"

REGEX_STAT_TERMINATOR = r"[\t ]*\}"

REGEX_LIST = [
    r"[\t ]*\.base([\w]*)[ \t=]*([\w]*)",  # (statname) (stat)
    r"[\t ]*\.([\w]*[\d])[ \t=]*TYPE_([\w]*)",  # (type1/type2) (type)
    r"[\t ]*\.(catchRate)[ \t=]*([\w]*)",  # ("catchRate") (rate)
    r"[\t ]*\.(expYield)[ \t=]*([\w]*)",  # (expYield) (yield)
    r"[\t ]*\.(evYield_[\w]*)[ \t=]*([\w]*)",  # (evYield_statname) (EVs)
    r"[\t ]*\.(item\d)[ \t=]*ITEM_([\w]*)",  # (item1/item2) (item)
    r"[\t ]*\.(genderRatio)[ \t=]*[\w]*\(([\d\.]*)",  # ("genderRatio") (ratio)
    # ("genderRatio") (ratio) for genderless mons
    r"[\t ]*\.(genderRatio)[ \t=]*MON_([\w]*)",
    r"[\t ]*\.(eggCycles)[ \t=]*([\w]*)",  # ("eggCycles") (eggcycles)
    r"[\t ]*\.(friendship)[ \t=]*([\w]*)",  # ("friendship") (friendship)
    r"[\t ]*\.(growthRate)[ \t=]*GROWTH_([\w]*)",  # ("growthRate") (rate)
    # ("eggGroup 1/2") (egg group)
    r"[\t ]*\.(eggGroup\d)[ \t=]*EGG_GROUP_([\w]*)",
    r"[\t ]*\.(ability\d)[ \t=]*ABILITY_([\w]*)",  # ("ability 1/2") (ability)
    # ("safariZoneFleeRate") (rate)
    r"[\t ]*\.(safariZoneFleeRate)[ \t=]*([\w]*)",
    # ("hiddenAbility") (ability)
    r"[\t ]*\.(hiddenAbility)[ \t=]*ABILITY_([\w]*)",
    # ("noFlip") (TRUE) apparently always true ????
    r"[\t ]*\.(noFlip)[ \t=]*([\w]*)"
]


while True:
    line = level.readline()
    pokeName = re.search(REGEX_FIRST_LINE, line)

    if pokeName != None:
        temp_name = (pokeName.group(1))  # getting the name of the pokemon
        if temp_name == "NONE":
            continue

        if temp_name[-2:] == "_A":
            temp_name = "ALOLAN " + temp_name[:-2]
        elif temp_name[-2:] == "_G":
            temp_name = "GALARIAN " + temp_name[:-2]
        elif temp_name[-2:] == "_H":
            temp_name = "HISUIAN " + temp_name[:-2]
        elif len(temp_name) > 4 and temp_name[-4:] == "MEGA":
            temp_name = "MEGA " + temp_name[:-4]
        elif len(temp_name) > 6 and temp_name[-6:] == "MEGA_X":
            temp_name = "MEGA " + temp_name[:-6] + " X"
        elif len(temp_name) > 6 and temp_name[-6:] == "MEGA_Y":
            temp_name = "MEGA " + temp_name[:-6] + " Y"
        elif temp_name[-2:] == "_M":
            temp_name = temp_name[:-2] + " MALE"
        elif temp_name[-2:] == "_F":
            temp_name = temp_name[:-2] + " FEMALE"

        if temp_name[-3:] == "_B_":  # to handle the "mega beta garchomp" case
            temp_name = "BETA " + temp_name[:-3]
        elif temp_name[-2:] == "_B":  # to handle the "beta garchomp" case
            temp_name = "BETA " + temp_name[:-2]

        temp_name = temp_name.replace('_', ' ')
        temp_dict['name'] = temp_name

        while True:  # iterate till we finish encountering the entire list
            if re.search(REGEX_STAT_TERMINATOR, line) != None:  # end of block
                if (len(temp_stats.keys()) == 29): # to ignore the "MANAPHY EGG", that shit has no stats just .noFlip = TRUE    
                    temp_stats['BST'] = int(temp_stats['HP']) + int(temp_stats['Attack']) + int(temp_stats['Defense']) + \
                        int(temp_stats['SpAttack']) + \
                        int(temp_stats['SpDefense']) + int(temp_stats['Speed'])

                    temp_dict['stats'] = temp_stats
                    overAllStats.append(temp_dict)
                temp_stats = {}
                temp_dict = {}
                break
            
            for r in REGEX_LIST:
                stats = re.search(r, line)
                if stats != None:  # match found
                    if stats.group(1) == "genderRatio":
                        if stats.group(2) == "GENDERLESS":
                            ans = "GENDERLESS"
                        else:
                            femPrec = float(stats.group(2))
                            malePerc = 100 - femPrec
                            ans = f'{femPrec}% female, {malePerc}% male'
                        temp_stats[stats.group(1)] = ans
                    else:
                        temp_stats[stats.group(1)] = stats.group(2)

            line = level.readline()
            if line == None:
                break
    if not line:
        break

print(len(overAllStats))

with open("extractor\stats\Base_Stats.json", "w", encoding="utf-8") as outfile:
    json.dump(overAllStats, outfile, indent=2)
