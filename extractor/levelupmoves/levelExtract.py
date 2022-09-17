import re
import json
level = open("extractor\levelupmoves\Learnsets.c", "r")

count = 0
overAllMoves = []
temp_name = ""
temp_moves = []
temp_dict = {}
REGEX_FIRST_LINE = r"\t*.*LevelUpMove[ ]*s([a-zA-Z_\.\- _]*)(LevelUpLearnset|Moveset)"
REGEX_MOVE_IDENTIFICATION = r"[\t ]*LEVEL_UP_MOVE[ ]*\([ ]*(\d*)[ ]*\,[ ]*MOVE_(\w*)"
REGEX_MOVE_TERMINATOR = r"[\t ]*LEVEL_UP_END"
while True:
    line = level.readline()

    pokeName = re.search(REGEX_FIRST_LINE, line)
    if pokeName != None:
        temp_name = (pokeName.group(1))  # getting the name of the pokemon

        if temp_name[-1] == "G":
            temp_name = "Galarian " + temp_name[:-1]
        elif temp_name[-1] == "A":
            temp_name = "Alolan " + temp_name[:-1]
        elif temp_name[-1] == "H":
            temp_name = "Hisuian " + temp_name[:-1]
        temp_dict['name'] = temp_name

        while True:  # iterate till we encounter LEVEL_UP_END
            lvlTerminator = re.search(REGEX_MOVE_TERMINATOR, line)
            if lvlTerminator != None:  # LEVEL_UP_END encountered
                if len(temp_moves) > 0:
                    temp_dict['lvlUpMoves'] = temp_moves
                    overAllMoves.append(temp_dict)
                temp_moves = []
                temp_dict = {}  # clearing them up
                break
            lvlMoves = re.search(REGEX_MOVE_IDENTIFICATION, line)
            if lvlMoves != None:  # moves found
                lvl_move_pair = [lvlMoves.group(1), lvlMoves.group(2)]
                temp_moves.append(lvl_move_pair)

            line = level.readline()
            if line == None:
                break
    if not line:
        break

print(len(overAllMoves))

with open("extractor\levelupmoves\Learnsets.json", "w", encoding="utf-8") as outfile:
    json.dump(overAllMoves, outfile, indent=2)
