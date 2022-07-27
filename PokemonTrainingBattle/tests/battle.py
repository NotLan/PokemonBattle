import pytest

from page_objects.pvpoke_page import *
from helpers.generate_pokemon_list import *


class TestBattle:

    @pytest.fixture()
    def training_battle_page(self, page) -> PvPokePage:
        """
        Navigates to the pvpoke battle page
        """
        pokemon_page = PvPokePage(page)
        pokemon_page.go_to_site()
        return pokemon_page

    def test_pokemon_battle(self, training_battle_page):
        """
        Picks two pokemon from the json list we give it (../pokemon-list.json
        Sets the users pokemon via the UI
        Sets the opponents pokemon via the UI
        Sets no shields for both
        Clicks battle
        Finds out if the users pokemon won or lost and logs to the user
        Then the battle is logged to ../battle_outcomes.json
        """
        picked_pokemon = pick_random_two_pokemon()
        training_battle_page.select_users_pokemon(pokemon_list=picked_pokemon)
        training_battle_page.select_opponents_pokemon(pokemon_list=picked_pokemon)
        training_battle_page.click_no_shields()
        training_battle_page.click_no_opponent_shield()
        training_battle_page.click_battle()
        winner, loser = training_battle_page.who_won(picked_pokemon)
        stats = training_battle_page.pull_stats()
        write_outcome_down(stats, winner, loser)
