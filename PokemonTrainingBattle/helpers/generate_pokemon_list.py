import json

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


def write_out_come_down(battle_outcome):
    data = json.load("battle_outcomes.json")
    open(data, "r")
    json.dump(data, file)


