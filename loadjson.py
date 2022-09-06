import json
from operator import truediv
import os
import numpy as np
import pandas as pd
import re
import constants

with open("DATA/abilities.json", encoding='utf8') as file:
    # you get a list of dictionaries, where each dictionary is like {'name', 'Ability'} and ability is a list
    ab = json.load(file)


# you get a normalized list of names from this (no capitals, removes everyhing in the regex)
ind = [re.sub(constants.normalize_regex, "", x['name']).lower() for x in ab]
# makes a dictionary out of 2 lists with a sturcture like [string, dictionary]
ab_dict = dict(zip(ind, ab))

# print(type(ab_dict['enamorus']['Ability']))


print(type(ab))
print(type(ab[0]))
