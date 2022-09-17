from audioop import add
import re
import constants
import math
# removes all blank spaces, underscores, slash and dash.


def normalizeString(text):  # removes
    return re.sub(constants.normalize_regex, "", text).lower()

# overloaded function to format the interpolated string, {}'s -> parameters.


def StringFormatter(str, a, b, c, d=None, e=None, f=None):
    if d != None:
        return str.format(a, b, c, d, e, f)
    else:
        return str.format(a, b, c)


# takes the specified column, normalizes it, then turns the list into a dictionary with key as normalized column, and value as list elements
def listToDict(columnToUseAsIndex, listToConvert):
    indices = [re.sub(constants.normalize_regex, "", x[columnToUseAsIndex]).lower()
               for x in listToConvert]  # getting the normalized list
    return dict(zip(indices, listToConvert))  # stitching them together


def calcScaledStats(data):  # replace this with the formula
    data = [int(x) for x in data]
    hp = data[0]
    if hp == 1:
        return data
    bst = data[6]

    before_scale = data[1:6]

    multiplier = (600.0-float(hp)) / (float(bst)-float(hp))

    after_stats = [min(255, math.floor(multiplier * x)) for x in before_scale]

    return [hp] + after_stats + [sum(after_stats) + hp]


# returns a formatted string with the pokemon data from stats.json (name, types, stats, generation etc)
def generateStatScreen(data):
    return constants.stat_display.format(data)

# splits the message into 3 groups, prefix + command(1 word, only alphabets, no spaces/special chars) + (rest of the string)


def msgSplitter(msg, reg):
    if match := re.search(reg, msg, re.IGNORECASE):
        title = match.groups()
        if len(title) <= 1:
            return False
        return [normalizeString(x) for x in title]

    return False


# li = [1,2,3,4,5,6,7]

# print(li[5])
# print(li[0])
# print(li[1:6])


# sss = '{} hello world {} {} {}'
# li = [1,3]
# li2 = [2,4]
# print(sss.format(*[li  + li2]))


# if scaleORnot is true, calc scalemon stats
def getComplexStats(element, scaleORnot=False):

    mon_stats = [element['HP'],
                 element['Attack'],
                 element['Defense'],
                 element['SpAttack'],
                 element['SpDefense'],
                 element['Speed'],
                 element['BST']]

    if scaleORnot == True:
        stat_template = constants.pokemon_stat_template.format(
            *calcScaledStats(mon_stats))
    else:
        stat_template = constants.pokemon_stat_template.format(*mon_stats)

    if element['type1'] == element['type2']:
        type_template = constants.pokemon_type_template.format(
            element['type1'].title())
    else:
        type_template = constants.pokemon_type_template.format(
            element['type1'].title() + ", " + element['type2'].title())

    capture_template = constants.pokemon_capture_template.format(element['catchRate'],
                                                                 element['expYield'])

    ev_yields_template = constants.pokemon_ev_yields_template.format(element["evYield_HP"],
                                                                     element["evYield_Attack"],
                                                                     element["evYield_Defense"],
                                                                     element["evYield_SpAttack"],
                                                                     element["evYield_SpDefense"],
                                                                     element["evYield_Speed"])

    item_template = constants.pokemon_item_template.format(element["item1"].title(),
                                                           element["item2"].title())

    if element['eggGroup1'] == element['eggGroup2']:
        eg = element['eggGroup1'].title()
    else:
        eg = element['eggGroup1'].title() + \
            ", " + element['eggGroup2'].title()

    breeding_template = constants.pokemon_breeding_template.format(element["genderRatio"].title(),
                                                                   element["eggCycles"],
                                                                   eg)
    ability_template = constants.pokemon_ability_template.format(element['ability1'].title(),
                                                                 element['ability2'].title(),
                                                                 element['hiddenAbility'].title())

    characteristics_template = constants.pokemon_characteristics_template.format(element['friendship'],
                                                                                 element['growthRate'].title())

    return [stat_template,
            type_template,
            capture_template,
            ev_yields_template,
            item_template,
            breeding_template,
            ability_template,
            characteristics_template]


def addFieldToEmbeds(emb, items, messages):
    for (i, m) in zip(items, messages):
        emb.add_field(
            name=f'__{m}__',
            value=i,
            inline=False
        )
    return emb
