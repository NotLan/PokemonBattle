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

    # Check to see if winner has battled before, If not write 1 win and 0 losses
    if dictObj.get(f"{winner}") is None:
        battle_outcome[f"{winner}"]["Wins"] = 1
        battle_outcome[f"{winner}"]["Losses"] = 0
    # If the winner has battled before, find out the number of wins and increment by +1 and write
    else:
        battle_outcome[f"{winner}"]["Wins"] = dictObj.get(f"{winner}")["Wins"]
        battle_outcome[f"{winner}"]["Wins"] += 1
        # If the winner losses is None write 0 to losses
        if dictObj.get(f"{winner}")["Losses"] is None:
            battle_outcome.get(f"{winner}")["Losses"] = 0
        # If the winner has losses, find out the number of losses and write
        else:
            battle_outcome.get(f"{winner}")["Losses"] = dictObj.get(f"{winner}").get("Wins")

    # Check to see if Loser has battled before, If not write 0 win and 1 losses
    if dictObj.get(f"{loser}") is None:
        battle_outcome[f"{loser}"]["Wins"] = 0
        battle_outcome[f"{loser}"]["Losses"] = 1
    # If the loser has battled before, find out he numbers of losses and increment by +1 and write
    else:
        battle_outcome[f"{loser}"]["Losses"] = dictObj.get(f"{loser}")["Losses"]
        battle_outcome[f"{loser}"]["Losses"] += 1
        # If the losers wins is None write 0 to wins
        if dictObj.get(f"{loser}")["Wins"] is None:
            battle_outcome[f"{loser}"]["Wins"] = 0
        # If the loser has wins, find out the number of losses and write
        else:
            battle_outcome.get(f"{loser}")["Wins"] = dictObj.get(f"{loser}").get("Wins")

    # Update .json with battle outcome
    dictObj.update(battle_outcome)

    # Dump to .json file
    with open("battle_outcomes.json", 'w') as json_file:
        json.dump(dictObj, json_file,
                  indent=4,
                  separators=(',', ': '))
