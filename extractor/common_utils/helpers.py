import re
normalize_regex = "[_\-\\\. ]+"

def listToDict(columnToUseAsIndex, listToConvert):
    indices = [re.sub(normalize_regex, "", x[columnToUseAsIndex]).lower()
               for x in listToConvert]  # getting the normalized list
    return dict(zip(indices, listToConvert))  # stitching them together

