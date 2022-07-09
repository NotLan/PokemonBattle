import pytest

from page_objects.pvpoke_page import *
from helpers.generate_pokemon_list import *
from page_objects.battle_page import BattlePage


class TestBattle:

    @pytest.fixture()
    def training_battle_page(self, page) -> PvPokePage:
        pokemon_page = PvPokePage(page)
        pokemon_page.go_to_site()
        return pokemon_page

    def test_battle(self, training_battle_page):
        picked_pokemon = pick_random_five_pokemon()
        my_pokemon = training_battle_page.select_my_pokemon(pokemon_list=picked_pokemon)
        opponent_pokemon = training_battle_page.select_opponent_pokemon(pokemon_list=my_pokemon)
        training_battle_page.click_no_shields()
        training_battle_page.click_no_opponent_shield()
        training_battle_page.click_opponent_random()
        training_battle_page.click_battle()
        stats = training_battle_page.pull_stats()
        assert my_pokemon in stats
