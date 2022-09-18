import re
import json
level = open("extractor\eggmoves\input\eggmoves.c", "r")

count = 0
overAllMoves = []
temp_name = ""
temp_moves = []
temp_dict = {}

REGEX_FIRST_LINE = r"[\t ]*egg_moves\(([\w]*)"
REGEX_MOVE_IDENTIFICATION = r"[\t ]*MOVE_([\w]*)[ \t]*,"
REGEX_MOVE_TERMINATOR = r"[\t ]*MOVE_([\w]*)\)"

while True:
    line = level.readline()

    pokeName = re.search(REGEX_FIRST_LINE, line)
    if pokeName != None:
        temp_name = (pokeName.group(1))  # getting the name of the pokemon

        if temp_name[-2:] == "_G":
            temp_name = "Galarian " + temp_name[:-2]
        elif temp_name[-2:] == "_A":
            temp_name = "Alolan " + temp_name[:-2]
        elif temp_name[-2:] == "_H":
            temp_name = "Hisuian " + temp_name[:-2]
        temp_dict['name'] = temp_name.title()

        while True:  # iterate till we encounter move_name),
            eggTerminator = re.search(REGEX_MOVE_TERMINATOR, line)
            if eggTerminator != None:  # move_name encountered
                em = eggTerminator.group(1)
                temp_moves.append(em)
                if len(temp_moves) > 0:
                    temp_dict['eggmoves'] = temp_moves
                    overAllMoves.append(temp_dict)
                temp_moves = []
                temp_dict = {}  # clearing them up
                break

            egg_move = re.search(REGEX_MOVE_IDENTIFICATION, line)
            if egg_move != None:  # moves found
                extracted_egg_move = egg_move.group(1)
                temp_moves.append(extracted_egg_move)

            line = level.readline()
            if line == None:
                break
    if not line:
        break

print(len(overAllMoves))

with open("extractor\eggmoves\output\eggmoves.json", "w", encoding="utf-8") as outfile:
    json.dump(overAllMoves, outfile, indent=2)
