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


def write_outcome_down(battle_outcome, who_won):
    with open("battle_outcomes.json") as fp:
        dictObj = json.load(fp)
    dictObj.update(battle_outcome)
    with open("battle_outcomes.json", 'w') as json_file:
        json.dump(dictObj, json_file,
                  indent=4,
                  separators=(',', ': '))
