## Introduction

This repo keeps updated resources about Pokémon, mainly Pokémon GO.

The POGO data and graphics come from [PokeMiners](https://github.com/PokeMiners). The data is converted to a few JSON files that are smaller and organized differently. The POGO graphics just get the filenames changed. Python scripts are used for collecting both POGO data and graphics.

These are the POGO data JSON files that are generated:
- `pogo_pkm.json`
- `pogo_cm.json`
- `pogo_fm.json`

There are also animated graphics, those are just manually collected from the internet.

## Instructions
Instructions in case you found something missing or outdated and you want to fix it - thank you for that!
### How to regularly update the POGO data
- Run `update_pogo_data.py` (when prompted, apply the manual patch)
- Check changes in `pogo_pkm.json`, `pogo_cm.json` and `pogo_fm.json`
- If everything looks good, you can commit and create a PR :-)
### How to add or remove manual changes to the POGO data
The POGO data comes directly from [PokeMiners Game Master](https://github.com/PokeMiners/game_masters). However, sometimes something is missing or wrong in the Game Master, or sometimes I just want to update it early. That's why there is a way to add a manual patch to the generated JSON files.
- Add or remove the changes to `pogo_pkm_manual.json`
  - Follow the system in place: Every change is an object with the `id`, `name` and `form` of the Pokémon to be changed and then the fields that need to change. The fields need to match those in `pogo_pkm.json`.
- Run `update_pogo_data.py` (when prompted, apply the manual patch)
- Check changes in `pogo_pkm.json`, `pogo_cm.json` and `pogo_fm.json`
- If everything looks good, you can commit and create a PR - commit the changes to `pogo_pkm_manual.json` as well :-)
### How to update the POGO graphics
- Go to the `graphics` directory and run `update_pogo_graphics.py`
- Check that the naming of the files makes sense according to the system followed and matches the existing animation graphics (if any) - use common sense!
- If everything looks good, you can commit and create a PR :-)

## Disclaimer
This repo is for educational use only. All content found within this repo is the property of The Pokémon Company and Niantic. All copyright belongs to the respective companies.
