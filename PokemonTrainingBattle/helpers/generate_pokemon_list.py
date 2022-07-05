import json

from pyotp import random


def load_pokemon_list():
    """

    :return:
    """
    x = json.open('pokemon.json')
    return json.load(x)


def pick_random_five_pokemon():
    """

    :return:
    """
    pokemon = load_pokemon_list()
    x = 5
    pokemon_list = []
    while x != 0:
        pokemon_list.append(random.choice(pokemon))
    return pokemon_list


