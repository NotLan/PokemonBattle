import json
from pyotp import random

def load_pokemon_list():
    return json.load(open('pokemon-list.json'))


def pick_random_two_pokemon():
    pokemon = load_pokemon_list()
    x = 2
    pokemon_list = []
    while x != 0:
        pokemon_list.append(random.choice(pokemon))
        x = x - 1
    return pokemon_list


def write_outcome_down(battle_outcome, winner, loser):
    with open("battle_outcomes.json") as fp:
        dictObj = json.load(fp)

    if dictObj.get(f"{winner}") is None:
        battle_outcome[f"{winner}"]["Wins"] = 1
        battle_outcome[f"{winner}"]["Losses"] = 0
    else:
        battle_outcome[f"{winner}"]["Wins"] += 1
        battle_outcome[f"{winner}"]["Losses"] = dictObj.get(f"{winner}")["Wins"]
        if dictObj.get(f"{winner}")["Losses"] is None:
            battle_outcome.get(f"{winner}")["Losses"] = 0
        else:
            battle_outcome.get(f"{winner}")["Losses"] = dictObj.get(f"{winner}").get("Wins")

    if dictObj.get(f"{loser}") is None:
        battle_outcome[f"{loser}"]["Wins"] = 0
        battle_outcome[f"{loser}"]["Losses"] = -1
    else:
        battle_outcome[f"{winner}"]["Wins"] = dictObj.get(f"{loser}")["Wins"]
        battle_outcome[f"{winner}"]["Losses"] -= 1
        if dictObj.get(f"{loser}")["Wins"] is None:
            battle_outcome[f"{loser}"]["Wins"] = 0
        else:
            battle_outcome.get(f"{loser}")["Wins"] = dictObj.get(f"{loser}").get("Wins")

    dictObj.update(battle_outcome)
    with open("battle_outcomes.json", 'w') as json_file:
        json.dump(dictObj, json_file,
                  indent=4,
                  separators=(',', ': '))
