import re
import json

f = open("extractor\moveinfo\input\moveDescription.txt", "r")
# f = open("dataextraction\\moves.json", "w")
flag = True
temp_dict = {}
moveList = []
count = 10
moveName = ""
moveDesc = ""
for x in f:
    x = x.replace("\\n", " ")
    x = x.replace("Pok\u00c3\u00a9mon", "Pokemon")

    # moveName = re.search(r"#\"?([\w\- _\.~\d]*)\"*#", x)
    move_and_description_beginning = re.search(
        r"#\"?([\w\- _\'\.~\d]*)\"*#.*\"([\d\w\-\'\.\, _]*)", x)
    move_and_desc_same_line = re.search(
        r"\#\"?([\d\w _\-\.\~]*)\"?\#.*[ ]*@{[ ]\"?([\-]*)\"?[ ]*@}", x)
    description_continued = re.search(r"(.*)", x)
    endOfLine = re.search(r"(.*)\"[ ]*@}", x)

    if move_and_desc_same_line != None:  # block with name and desc in the same line
        moveName = move_and_desc_same_line.group(1)
        if re.search(r"\~", moveName) != None:
            flag = False
            continue
        moveDesc = move_and_desc_same_line.group(2)
        temp_dict['movename'] = moveName
        temp_dict['movedesc'] = moveDesc
        moveName = ""
        moveDesc = ""
        moveList.append(temp_dict)
        temp_dict = {}

    elif move_and_description_beginning != None:  # start of a move block
        # print(move_and_description_beginning.group(1) + "      " + move_and_description_beginning.group(2) )
        moveName = move_and_description_beginning.group(1)
        if re.search(r"\~", moveName) != None:
            flag = False
            continue
        moveDesc = move_and_description_beginning.group(2)
    elif endOfLine != None:
        if flag == False:
            flag = True
            continue
        moveDesc += endOfLine.group(1)
        temp_dict['movename'] = moveName
        temp_dict['movedesc'] = moveDesc
        moveName = ""
        moveDesc = ""
        moveList.append(temp_dict)
        temp_dict = {}
    elif description_continued != None:
        if flag == False:
            continue
        moveDesc += description_continued.group(1)


with open("extractor\moveinfo\output\MOVE_DESCRIPTION.json", "w", encoding="utf-8") as outfile:
    json.dump(moveList, outfile, indent=2)

# name, effect, power, type, accuracy, pp, effectAccuracy, target, priority, info
temp_dict = {}
infoList = []
f = open("extractor\moveinfo\input\moveData.txt", "r")
index = 0
for x in f:
    move_info = re.search(
        r"\+\#\"?([ \.\-_\d\w\']*)\"?\#, ([\"\w ]*), ([\d]*), ([\d\w\?]*), ([\d\w]*), ([\d\w]*), ([\d\w]*), \- ([\w\d_ ]*)/, ([\-\d]*), \-([\"\d\w \-]*)/", x)
    if move_info != None:

        info = move_info.group(10)
        info = info.replace('" "', ", ").replace('"', '')

        temp_dict['movename'] = move_info.group(1)
        temp_dict['effect'] = move_info.group(2).replace('"', '')
        temp_dict['power'] = move_info.group(3)
        temp_dict['type'] =  "Fairy" if move_info.group(4) == "23" else move_info.group(4) 
        temp_dict['accuracy'] = move_info.group(5)
        temp_dict['pp'] = move_info.group(6)
        temp_dict['effectAccuracy'] = move_info.group(7)
        temp_dict['target'] = move_info.group(8)
        temp_dict['priority'] = move_info.group(9)
        temp_dict['info'] = info.strip()
        infoList.append(temp_dict)
        temp_dict = {}


with open("extractor\moveinfo\output\MOVE_INFO.json", "w", encoding="utf-8") as outfile:
    json.dump(infoList, outfile, indent=2)

print(len(moveList))

print(len(infoList))

moveList = sorted(moveList, key=lambda d: d['movename'])
infoList = sorted(infoList, key=lambda d: d['movename'])

mergedList=[]
for i,j in zip(moveList, infoList):
    mergedList.append(i|j)


with open("extractor\moveinfo\output\MOVE_MERGED.json", "w", encoding="utf-8") as outfile:
    json.dump(mergedList, outfile, indent=2)
# with open("dataextraction\\MOVE_MERGED.txt", "w", encoding="utf-8") as outfile:
#     json.dump(mergedList, outfile, indent=2)