import json
import pickle
from pyotp import random


def load_pokemon_list():
    """

    :return:
    """
    x = open('pokemon.json')
    return json.load(x)


def pick_random_five_pokemon():
    """

    :return:
    """
    pokemon = load_pokemon_list()
    x = 3
    pokemon_list = []
    while x != 0:
        pokemon_list.append(random.choice(pokemon))
        x = x - 1
    return pokemon_list


def write_outcome_down(battle_outcome):
    json1 = json.dumps(battle_outcome, indent=4)
    f = open("dict.json", "a")
    f.write(f"{json1}")
    f.close()

    # filehandler = open("battle_outcome.json", 'ab+')
    # pickle.dump(battle_outcome, filehandler)
    # filehandler.close()
