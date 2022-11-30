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

        filename = GetPokemonFilename(i)

        print("#" + str(i) + " " + filename + " [", end="")

        UpdatePokemon(DIR + filename, URL, i, False)
        UpdatePokemon(SHINY_DIR + filename, URL, i, True)
        UpdatePokemon(DIR_256 + filename, URL_256, i, False)
        UpdatePokemon(SHINY_DIR_256 + filename, URL_256, i, True)

        print("]")

def UpdatePokemon(path, base_url, pkm_id, is_shiny):

    if not exists(path):
        url = base_url + "pm" + str(pkm_id) + ("", ".s")[is_shiny] + ".icon.png"
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

def GetPokemonFilename(pkm_id):
    name = pokemon_names[str(pkm_id)]["name"]
    return (CleanStr(name) + ".png")

def CleanStr(string):
    return ("".join(filter(str.isalnum, string.lower())))

if __name__=="__main__":
    main()

