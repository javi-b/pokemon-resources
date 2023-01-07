# updates pogo assets from PokeMiners/pogo_assets in GitHub.
# sorts the assets following this repo structure and filenames system

import sys
import os
import subprocess
from os.path import exists
import json

# global constants and variables

MAX_ID = 905 # maximum pokemon id
URL = "https://raw.githubusercontent.com/PokeMiners/pogo_assets/master/Images/Pokemon/Addressable%20Assets/"
URL_256 = "https://raw.githubusercontent.com/PokeMiners/pogo_assets/master/Images/Pokemon%20-%20256x256/Addressable%20Assets/"
DIR = "pogo/"
SHINY_DIR = "pogo-shiny/"
DIR_256 = "pogo-256/"
SHINY_DIR_256 = "pogo-shiny-256/"

# parses pokemon names json file
pokemon_names = json.load(open("pokemon_names.json"))

def main():

    for i in range(1, MAX_ID + 1):

        filenames_pairs = GetPokemonFilenamesPairs(i)

        for pogo_filename, filename in filenames_pairs:

            print("#" + str(i) + " " + filename + " [", end="")

            UpdatePokemon(URL, pogo_filename, DIR + filename, i, False)
            UpdatePokemon(URL, pogo_filename, SHINY_DIR + filename, i, True)
            UpdatePokemon(URL_256, pogo_filename, DIR_256 + filename, i, False)
            UpdatePokemon(URL_256, pogo_filename, SHINY_DIR_256 + filename, i, True)

            print("]")

def UpdatePokemon(base_url, pogo_filename, path, pkm_id, is_shiny):
    if not exists(path):
        url = base_url + pogo_filename
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

def GetPokemonFilenamesPairs(pkm_id):
    """ Gets a list of pairs of filenames.
    The first filename is used to download the pokemon go asset,
    the second one is the filename saved on disk following the local
    name convention.
    """

    MEGA_PKMS = { 3, 6, 9, 15, 18, 65, 80, 94, 115, 127, 130, 142, 150,
            181, 208, 212, 214, 229, 248, 254, 260, 257, 282, 302, 303,
            308, 306, 310, 319, 323, 334, 354, 359, 362, 373, 376, 380,
            384, 381, 428, 445, 448, 460, 475, 531, 719 }
    ALOLA_FORM_PKMS = { 19, 20, 26, 27, 28, 37, 38, 50, 51, 52, 53, 74, 75, 
            76, 88, 89, 103, 105 }
    GALARIAN_FORM_PKMS = { 52, 77, 78, 79, 80, 83, 110, 122, 144, 145, 146,
            199, 222, 263, 264, 554, 562, 618 }
    HISUIAN_FORM_PKMS = { 58, 59, 100, 101, 157, 211, 215, 503, 549, 570,
            571, 628, 705, 706, 713, 724 }

    filenames_pairs = [];

    pogo_filename = "pm" + str(pkm_id) + ".icon.png"
    name = CleanStr(pokemon_names[str(pkm_id)]["name"])
    filenames_pairs.append([pogo_filename, name + ".png"])

    if (pkm_id in MEGA_PKMS):
        pogo_filename = "pm" + str(pkm_id) + ".fMEGA.icon.png"
        filenames_pairs.append([pogo_filename, name + "-mega.png"])
    if (pkm_id in ALOLA_FORM_PKMS):
        pogo_filename = "pm" + str(pkm_id) + ".fALOLA.icon.png"
        filenames_pairs.append([pogo_filename, name + "-alola.png"])
    if (pkm_id in GALARIAN_FORM_PKMS):
        pogo_filename = "pm" + str(pkm_id) + ".fGALARIAN.icon.png"
        filenames_pairs.append([pogo_filename, name + "-galar.png"])
    if (pkm_id in HISUIAN_FORM_PKMS):
        pogo_filename = "pm" + str(pkm_id) + ".fHISUIAN.icon.png"
        filenames_pairs.append([pogo_filename, name + "-hisuian.png"])

    return filenames_pairs

def CleanStr(string):
    return ("".join(filter(str.isalnum, string.lower())))

if __name__=="__main__":
    main()

