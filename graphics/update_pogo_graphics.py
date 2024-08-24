# updates pogo graphics from PokeMiners/pogo_assets in GitHub.
# sorts the graphics following this repo structure and filenames system

import urllib.request
import sys
import os
import subprocess
from os.path import exists
import json

# global constants and variables

URL_GAME_MASTER = "https://raw.githubusercontent.com/PokeMiners/game_masters/master/latest/latest.json"

URL = "https://raw.githubusercontent.com/PokeMiners/pogo_assets/master/Images/Pokemon/Addressable%20Assets/"
URL_256 = "https://raw.githubusercontent.com/PokeMiners/pogo_assets/master/Images/Pokemon%20-%20256x256/Addressable%20Assets/"
DIR = "pogo/"
SHINY_DIR = "pogo-shiny/"
DIR_256 = "pogo-256/"
SHINY_DIR_256 = "pogo-shiny-256/"

# parses pokemon names json file
pokemon_names = json.load(open("../pokemon_names.json"))

def main():

    print("loading game master...")
    game_master = json.load(urllib.request.urlopen(URL_GAME_MASTER))
    print("downloading nonexisting graphics...")
    for gm_obj in game_master:
        id = gm_obj["templateId"]
        if id[0] == "V" and id[6:13] == "POKEMON" and id.find("REVERSION") == -1:
            filenames_pairs = GetFilenamesPairs(gm_obj)
            for pm_filename, filename in filenames_pairs:
                print(pm_filename + " -> " + filename + " [", end="")
                UpdatePokemon(URL + pm_filename, DIR + filename, False)
                UpdatePokemon(URL + pm_filename, SHINY_DIR + filename, True)
                UpdatePokemon(URL_256 + pm_filename, DIR_256 + filename, False)
                UpdatePokemon(URL_256 + pm_filename, SHINY_DIR_256 + filename, True)
                print("]")

    os.system("pause")

def GetFilenamesPairs(gm_obj):

    filenames_pairs = [];

    gm_obj_s = gm_obj["data"]["pokemonSettings"]
    id = int(gm_obj["templateId"][1:5])
    name = CleanStr(pokemon_names[str(id)]["name"])
    if id == 29: # female Nidoran
        name += "f"
    elif id == 32: # male Nidoran
        name += "m"

    # name
    pm_filename = "pm" + str(id)
    filename = name

    # form
    # set of pokemon who contain a form named Normal
    NORMAL_FORMS_IDS = {649}
    # set of pokemon whose names are part of their form in 'pm_filename'
    NAMES_IN_FORM_IDS = {201, 412, 413}
    if "form" in gm_obj_s and isinstance(gm_obj_s["form"], str) \
            and (gm_obj_s["form"][-7:] != "_NORMAL" or id in NORMAL_FORMS_IDS):
        form = gm_obj_s["form"]
        if gm_obj_s["pokemonId"] in form and id not in NAMES_IN_FORM_IDS:
            form = form.replace(gm_obj_s["pokemonId"], "")[1:]
        pm_filename += ".f" + form;
        if id in NAMES_IN_FORM_IDS:
            form = form.replace(gm_obj_s["pokemonId"], "")
        filename += "-" + CleanStr(form)

    # suffix
    pm_filename += ".icon.png"
    filename += ".png";

    filenames_pairs.append((pm_filename, filename))

    # extra mega filenames pairs
    if "tempEvoOverrides" in gm_obj_s:
        if id == 6 or id == 150: # Charizard or Mewtwo
            filenames_pairs.append(("pm"+str(id)+".fMEGA_X.icon.png", name+"-megax.png"))
            filenames_pairs.append(("pm"+str(id)+".fMEGA_Y.icon.png", name+"-megay.png"))
        elif id == 382 or id == 383: # Kyogre or Groudon
            filenames_pairs.append(("pm"+str(id)+".fPRIMAL.icon.png", name+"-primal.png"))
        else:
            filenames_pairs.append(("pm"+str(id)+".fMEGA.icon.png", name+"-mega.png"))

    return filenames_pairs;

def UpdatePokemon(url, path, is_shiny):
    if not exists(path):
        if (is_shiny):
            insert_point = url.find(".icon.png")
            url = url[:insert_point] + ".s" + url[insert_point:]
        res = subprocess.call(["curl", "-f", url, "-o", path],
                stdout=open(os.devnull, "w"),
                stderr=subprocess.STDOUT)
        if (res == 0):
            print(".", end="")
        elif (res == 22):
            print("    x    ", end="")
    else:
        print("-", end="")
    sys.stdout.flush()

def CleanStr(string):
    return ("".join(filter(str.isalnum, string.lower())))

if __name__=="__main__":
    main()

