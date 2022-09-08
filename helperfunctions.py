import re
import constants

# removes all blank spaces, underscores, slash and dash.


def normalizeString(text): # removes 
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


def calcScaledStats(bst, hp, at, df, sp, spd, spe):  # replace this with the formula
    return bst + hp + at + df + sp + spd + spe


# returns a formatted string with the pokemon data from stats.json (name, types, stats, generation etc)
def generateStatScreen(data):
    return constants.stat_display.format(*(data.values()))

# splits the message into 3 groups, prefix + command(1 word, only alphabets, no spaces/special chars) + (rest of the string)

def msgSplitter(msg, reg):
    if match := re.search(reg, msg, re.IGNORECASE):
        title = match.groups()
        if len(title) <=1:
            return False 
        return [ normalizeString(x) for x in title]

    return False
