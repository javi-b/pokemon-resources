import urllib.request
import requests
import lxml.html
import json

# global constants and variables

URL_GAME_MASTER = "https://raw.githubusercontent.com/PokeMiners/game_masters/master/latest/latest.json"

URL_UNUSED = "https://pokeminers.com/unusedfindings/"

JSON_PKM_PATH = "pogo_pkm.json"
JSON_FM_PATH = "pogo_fm.json"
JSON_CM_PATH = "pogo_cm.json"

pokemon_names = json.load(open("pokemon_names.json"))

pogo_unused = {} # sets of unused pokemon, forms, shadows and moves

pogo_pkm = [] # pogo pokemon object, will become json file
pogo_fm = [] # pogo fast moves object, will become json file
pogo_cm = [] # pogo charged moves object, will become json file

def main():

    # scrapes relevant unused lists from pokeminers.com into 'pogo_unused'
    print("scraping " + URL_UNUSED + "...")
    html = lxml.html.fromstring(requests.get(URL_UNUSED).content)
    ScrapeList(html, '//ul[@id="Pokémon-list"]/li/text()', 'pokemon')
    ScrapeList(html, '//ul[@id="Forms-list"]/li/text()', 'forms')
    ScrapeList(html, '//ul[@id="Shadows-list"]/li/text()', 'shadows')
    ScrapeList(html, '//ul[@id="Moves-list"]/li/text()', 'moves')

    # creates jsons
    print("loading game master...")
    game_master = json.load(urllib.request.urlopen(URL_GAME_MASTER))
    print("creating JSON files...")
    for gm_obj in game_master:
        id = gm_obj["templateId"]
        if id[0] == "V" and id[6:13] == "POKEMON" and id.find("REVERSION") == -1:
            AddPokemon(gm_obj)
        if id[0] == "V" and id[6:10] == "MOVE":
            AddMove(gm_obj, id[-4:] == "FAST")
    json.dump(pogo_pkm, open(JSON_PKM_PATH, "w"), indent=4)
    json.dump(pogo_fm, open(JSON_FM_PATH, "w"), indent=4)
    json.dump(pogo_cm, open(JSON_CM_PATH, "w"), indent=4)

def ScrapeList(html, xpath, name):
    lis = html.xpath(xpath)
    pogo_unused[name] = set()
    for li in lis:
        pkm = li.replace(' ', '').replace('\n', '').replace('\r', '')
        pogo_unused[name].add(pkm)
    print(" " + str(len(lis)) + " unused " + name + " found")

def AddPokemon(gm_obj):

    #print(gm_obj["templateId"])

    gm_obj_s = gm_obj["data"]["pokemonSettings"]

    pkm_obj = {}
    pkm_obj["id"] = int(gm_obj["templateId"][1:5])
    pkm_obj["name"] = pokemon_names[str(pkm_obj["id"])]["name"]
    if "form" in gm_obj_s and isinstance(gm_obj_s["form"], str):
        form = gm_obj_s["form"]
        if gm_obj_s["pokemonId"] in form:
            form = form.replace(gm_obj_s["pokemonId"], "")[1:]
        pkm_obj["form"] = form.capitalize()
    else:
        pkm_obj["form"] = "Normal"
    pkm_obj["types"] = []
    pkm_obj["types"].append(CleanType(gm_obj_s["type"]))
    if "type2" in gm_obj_s:
        pkm_obj["types"].append(CleanType(gm_obj_s["type2"]))
    pkm_obj["stats"] = gm_obj_s["stats"]
    if "quickMoves" in gm_obj_s:
        pkm_obj["fm"] = CleanMoves(gm_obj_s["quickMoves"], True)
    if "cinematicMoves" in gm_obj_s:
        pkm_obj["cm"] = CleanMoves(gm_obj_s["cinematicMoves"], False)
    if "eliteQuickMove" in gm_obj_s:
        pkm_obj["elite_fm"] = CleanMoves(gm_obj_s["eliteQuickMove"], True)
    if "eliteCinematicMove" in gm_obj_s:
        pkm_obj["elite_cm"] = CleanMoves(gm_obj_s["eliteCinematicMove"], False)
    pkm_obj["shadow"] = "shadow" in gm_obj_s
    if pkm_obj["shadow"]:
        pkm_obj["shadow_released"] = (gm_obj["templateId"][14:] + "_SHADOW") not in pogo_unused["shadows"]
    else:
        pkm_obj["shadow_released"] = False
    mega_objs = []
    if "tempEvoOverrides" in gm_obj_s:
        for gm_obj_s_mega in gm_obj_s["tempEvoOverrides"]:
            mega_obj = {}
            mega_types = []
            if "typeOverride1" in gm_obj_s_mega:
                mega_types.append(CleanType(gm_obj_s_mega["typeOverride1"]))
            if "typeOverride2" in gm_obj_s_mega:
                mega_types.append(CleanType(gm_obj_s_mega["typeOverride2"]))
            if mega_types:
                mega_obj["types"] = mega_types
            if "stats" in gm_obj_s_mega:
                mega_obj["stats"] = gm_obj_s_mega["stats"]
            if mega_obj:
                mega_objs.append(mega_obj)
    if mega_objs:
        pkm_obj["mega"] = mega_objs
    if "pokemonClass" in gm_obj_s:
        pkm_obj["class"] = gm_obj_s["pokemonClass"]
    pkm_obj["released"] = PokemonIsReleased(gm_obj_s)

    pogo_pkm.append(pkm_obj)

def PokemonIsReleased(gm_obj_s):
    released = gm_obj_s["pokemonId"] not in pogo_unused["pokemon"]
    if released and "form" in gm_obj_s:
        released = gm_obj_s["form"] not in pogo_unused["forms"]
    return released

def AddMove(gm_obj, is_fast):

    #print(gm_obj["templateId"])

    gm_obj_s = gm_obj["data"]["moveSettings"]

    move_obj = {}
    move_obj["name"] = CleanMove(gm_obj_s["movementId"], is_fast)
    move_obj["type"] = CleanType(gm_obj_s["pokemonType"])
    if "power" in gm_obj_s:
        move_obj["power"] = gm_obj_s["power"]
    else:
        move_obj["power"] = 0
    move_obj["duration"] = gm_obj_s["durationMs"]
    move_obj["damage_window_start"] = gm_obj_s["damageWindowStartMs"]
    move_obj["damage_window_end"] = gm_obj_s["damageWindowEndMs"]
    if "energyDelta" in gm_obj_s:
        move_obj["energy_delta"] = gm_obj_s["energyDelta"]
    else:
        move_obj["energy_delta"] = 0

    if is_fast:
        pogo_fm.append(move_obj)
    else:
        pogo_cm.append(move_obj)

def CleanType(type):
    return type[13:].capitalize()

def CleanMoves(moves, is_fast):
    clean_moves = []
    for move in moves:
        clean_moves.append(CleanMove(move, is_fast))
    return clean_moves

def CleanMove(move, is_fast):
    return (move[:-5] if is_fast else move).replace("_", " ").title()

if __name__=="__main__":
    main()