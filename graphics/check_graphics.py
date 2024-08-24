# checks graphics in local repository
# and helps finding missing ones and getting other useful information

import urllib.request
import os
from os.path import exists
import json

# global constants and variables

URL_GAME_MASTER = "https://raw.githubusercontent.com/PokeMiners/game_masters/master/latest/latest.json"

DIRS = ("ani", "ani-shiny", "pogo", "pogo-shiny", "pogo-256", "pogo-shiny-256")

# parses pokemon names json file
pokemon_names = json.load(open("../pokemon_names.json"))

total = 0 # total number of pokemon searched for
found_in_each_dir = {} # number of pokemon found in each DIR
for DIR in DIRS:
    found_in_each_dir[DIR] = 0
not_found_total = 0 # total number of pokemon not found at all

def main():

    global total

    # loads game master 
    print("loading game master...")
    game_master = json.load(urllib.request.urlopen(URL_GAME_MASTER))

    # checks pokemon and prints missing ones
    print("checking graphics... (missing graphics will be printed)")
    header = "[ "
    for DIR in DIRS:
        header += "(" + DIR + ") "
    header += "]"
    print(header)
    for gm_obj in game_master:
        id = gm_obj["templateId"]
        if id[0] == "V" and id[6:13] == "POKEMON" and id.find("REVERSION") == -1:
            filenames = GetFilenames(gm_obj)
            for pkm_id, filename in filenames:
                CheckPokemon(DIRS, pkm_id, filename)
                total += 1
    
    # prints summary
    print("".rjust(20) + "found".ljust(10))
    print("".rjust(20) + "-----".ljust(10))
    for DIR in DIRS:
        total_pct = round(100 * found_in_each_dir[DIR] / total, 2)
        print((DIR + " ").rjust(20) + (str(total_pct) + "%").ljust(10))
    not_found_pct = round(100 * not_found_total / total, 2)
    print("".ljust(40) + str(not_found_pct) + "% not found in any directory")

    os.system("pause")

def GetFilenames(gm_obj):

    filenames = [];

    gm_obj_s = gm_obj["data"]["pokemonSettings"]
    id = int(gm_obj["templateId"][1:5])
    name = CleanStr(pokemon_names[str(id)]["name"])
    if id == 29: # female Nidoran
        name += "f"
    elif id == 32: # male Nidoran
        name += "m"

    # name
    filename = name

    # form
    # set of pokemon who contain a form named Normal
    NORMAL_FORMS_IDS = {649}
    if "form" in gm_obj_s and isinstance(gm_obj_s["form"], str) \
            and (gm_obj_s["form"][-7:] != "_NORMAL" or id in NORMAL_FORMS_IDS):
        form = gm_obj_s["form"]
        if gm_obj_s["pokemonId"] in form:
            form = form.replace(gm_obj_s["pokemonId"], "")[1:]
        filename += "-" + CleanStr(form)

    filenames.append((id, filename))

    # extra mega filenames
    if "tempEvoOverrides" in gm_obj_s:
        if id == 6 or id == 150: # Charizard or Mewtwo
            filenames.append((id, name+"-megax"))
            filenames.append((id, name+"-megay"))
        elif id == 382 or id == 383: # Kyogre or Groudon
            filenames.append((id, name+"-primal"))
        else:
            filenames.append((id, name+"-mega"))

    return filenames;

def CheckPokemon(DIRS, pkm_id, filename):
    should_print = False
    not_found = True
    global not_found_total
    text = ("#" + str(pkm_id) + " " + filename).ljust(40) + "["
    for DIR in DIRS:
        path = DIR + "/" + filename + (".gif" if "ani" in DIR else ".png")
        if exists(path):
            text += "-"
            not_found = False
            found_in_each_dir[DIR] += 1
        else:
            text += "x"
            should_print = True
    if should_print:
        text += "]"
        print(text)
    if not_found:
        not_found_total += 1

def CleanStr(string):
    return ("".join(filter(str.isalnum, string.lower())))

if __name__=="__main__":
    main()
