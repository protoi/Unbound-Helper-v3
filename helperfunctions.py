import re
import constants
# removes all blank spaces, underscores, slash and dash.


def normalizeString(text):
    return re.sub("[_\-\\ ]+", "", text).lower()

# overloaded function to format the interpolated string, {}'s -> parameters.


def StringFormatter(str, a, b, c, d, e, f):
    return str.format(a, b, c, d, e, f)


def StringFormatter(str, a, b, c):
    return str.format(a, b, c)


def listToDict(columnToUseAsIndex, listToConvert):
    i = [re.sub(constants.normalize_regex, "", x[columnToUseAsIndex]).lower() for x in listToConvert]
    return dict(zip(i, listToConvert))

