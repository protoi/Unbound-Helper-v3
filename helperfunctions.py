import re
import constants

# removes all blank spaces, underscores, slash and dash.


def normalizeString(text):
    return re.sub("[_\-\\ ]+", "", text).lower()

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
